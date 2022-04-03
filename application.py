import os
import click
from flask import Flask
from app import create_app, db, file
from app.models import User, Role, File



app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, File=File)
    # return dict(db=db, User=User, Role=Role, File=File, Appointment=Appointment, Patient=Patient, Doctor=Doctor)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

app.run(host='0.0.0.0', port=8000, debug=True)