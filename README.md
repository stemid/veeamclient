# VeeamClient

Python API for connecting to Veeam Backup RESTful API service.

Very much an unfinished product right now, only finished as far as I needed it.

# Install

	$ python setup.py install

# Examples

## Get a Veeam session.

	v = VeeamSession(
		username='secret',
		password='secret',
	)

## Get your session ID.

	v.session_id

The library will mostly return XML Element objects. Like here where you see all the current logon sessions.

	for session in v.logonSessions:
		print(session.find('veeam:UserName', v._ns).text)
		print(session.find('veeam:SessionId', v._ns).text)

## XML Namespace 

The Veeam API requires an XML namespace that is hard coded and defined as 'veeam' in this library. Use v.namespace to reference it.

You can also define your own prefix for the namespace. 

	v = VeeamSession(
		namespace='Veeam'
	)

## API Access

With the basic Enterprise license you won't be able to access all the API features documented. 

Get a list of the ones you can access.

	session = v.logonSession
	for link in session.find('veeam:Links', v.namespace):
		print(link.attrib.get('Href'))

The logon\_paths property shows a list of those paths that you can match against to see why you might be getting 403 access denied.

## More examples

See the list\_job\_statistics.py file in tests/ that lists the current job statistics of all backup servers.

Use repl.py for simple debugging, for example:

	$ ipython -i -- repl.py --config client.cfg

Lastly read the source, veeamclient.py should be pretty self-explanatory to python users.

# API Documentation

* [API Documentation](https://helpcenter.veeam.com/backup/rest/em_web_api_reference.html)
