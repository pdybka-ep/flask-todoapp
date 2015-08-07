from hitchserve import ServiceBundle, Service
from os import path, system, chdir
from subprocess import call, PIPE
import hitchenvironment
import hitchpostgres
import hitchselenium
import hitchpython
import hitchtest
import IPython
import sys
import time

# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class FlaskService(Service):
    def __init__(self, python, needs):
        self.python = python
        super(FlaskService, self).__init__(
            command=[python, "-u", path.join(PROJECT_DIRECTORY, "todoapp.py")],
            log_line_ready_checker=lambda line: "Running on" in line,
            needs=needs,
        )

    def setup(self):
        self.subcommand(self.python, path.join(PROJECT_DIRECTORY, "createdb.py")).run()


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Engine for orchestating and interacting with the TODO app."""
    def set_up(self):
        """Ensure python environment  present, then run all services."""
        python_package = hitchpython.PythonPackage(
            python_version=self.settings['python_version'],
            directory=path.join(
                PROJECT_DIRECTORY, "pyv{}".format(
                    self.settings['python_version']
                )
            )
        )
        python_package.build()
        python_package.verify()

        call([
            python_package.pip, "install", "-r",
            path.join(PROJECT_DIRECTORY, "requirements.txt")
        ])

        postgres_package = hitchpostgres.PostgresPackage(
            version=self.settings["postgres_version"],
        )
        postgres_package.build()
        postgres_package.verify()

        self.services = ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            startup_timeout=float(self.settings["startup_timeout"]),
            shutdown_timeout=5.0,
        )

        postgres_user = hitchpostgres.PostgresUser("patrycja", "mypassword")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            port=5432,
            postgres_package=postgres_package,
            users=[postgres_user, ],
            databases=[hitchpostgres.PostgresDatabase("todoapp", postgres_user), ]
        )

        self.services['Flask'] = FlaskService(
            python=python_package.python,
            needs=[self.services['Postgres'],]
        )

        self.services['Firefox'] = hitchselenium.SeleniumService(
            xvfb=self.settings.get("xvfb", False) or self.settings.get("quiet", False),
            no_libfaketime=True,
        )

        self.services.startup(interactive=False)

        # Configure selenium driver
        self.driver = self.services['Firefox'].driver
        self.driver.set_window_size(800, 600)
        self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(2.0)
        self.driver.accept_next_alert = True

    def pause(self, message=None):
        """Stop. IPython time."""
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
        self.ipython(message)
        if hasattr(self, 'services'):
            self.services.stop_interactive_mode()

    def load_website(self):
        """Navigate to website in Firefox."""
        time.sleep(0.5) # Turns out that flask isn't entirely truthful about when it is running
        self.driver.get("http://localhost:5000")

    def click(self, on):
        """Click on HTML id."""
        self.driver.find_element_by_id(on).click()

    def fill_form(self, **kwargs):
        """Fill in a form with id=value."""
        for element, text in kwargs.items():
            self.driver.find_element_by_id(element).send_keys(text)

    def time_travel(self, days=""):
        """Move services forward in time x days"""
        self.services.time_travel(days=int(days))

    def on_success(self):
        pass

    def on_failure(self):
        pass

    def tear_down(self):
        """Shut down all of the services."""
        if hasattr(self, 'services'):
            self.services.shutdown()
