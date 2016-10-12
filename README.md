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

	for session in v.logonSessions:
		print(session.find('veeam:UserName', v._ns).text)
		print(session.find('veeam:SessionId', v._ns).text)

The Veeam API requires an XML namespace that is hard coded and defined as 'veeam' in this library. Use v.api\_namespace to reference it.

You can also define your own prefix for the namespace. 

	v = VeeamSession(
		namespace='Veeam'
	)

See the list\_job\_statistics.py file in tests/ that lists the current job statistics of all backup servers.

Use repl.py for simple debugging, for example:

	$ ipython -i -- repl.py --username secret --read-password

Lastly read the source, veeamclient.py is pretty self-explanatory for any python-coder.
