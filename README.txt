This is an early version of the chat linker for WWU DC.
There is a threaded folder and a non-threaded folder.
Some things to be done to make this chat linker decent are listed below.

Things to be done:
	Make sure all features from the non-threaded version are working in the threaded version
	figure out what is and is not working
		communication between bots and server
		reading from dc chat and irc chat
		posting to dc chat and irc chat
	networking changes
		server sits on a single port waiting for a connection from a bot
		once bot connects use new "random" port for future communication with bot