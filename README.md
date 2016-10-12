# VeeamClient

Python API for connecting to Veeam Backup RESTful API service.

Very much an unfinished product right now, only finished as far as I needed it.

# Install

	$ python setup.py install

# Example

Get a Veeam session.

  v = VeeamSession(
		username='secret',
		password='secret',
	)

Get your session ID.

	v.session_id

The library will mostly return XML Element objects. Like here where you see all the current logon sessions.

	sessions = v.logonSessions
	for session in sessions:
		print(session.attrib.get('veeam:UserName', v.api_namespace), \
			session.attrib.get('veeam:SessionId', v.api_namespace))

The Veeam API requires an XML namespace that is hard coded and defined as 'veeam' in this library. Use v.api\_namespace to reference it.

You can also define your own prefix for the namespace. 

	v = VeeamSession(
		namespace='Veeam'
	)

See the list\_job\_statistics.py file in tests/ that lists the current job statistics of all backup servers.

Use repl.py for simple debugging, for example:

	$ ipython -i -- repl.py --username secret --read-password

Lastly read the source, veeamclient.py is pretty self-explanatory for any python-coder.
