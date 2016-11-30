					*-*  Always read the read me *-*

This briefly describes the code layout and functionality. 

Language
		Written in python2.7 
		make sure that  python in installed, open a cmd and type:
		     	  	
				       $ python --version ( vers. >= 2.7 )
Files 		
		testMain.py	Temporary test driver, serves as tool indicating function module proper execution. 
		main.py		Driver program.
		loadData.py	Used to initialize variables required for code execution.
		dijkstra.py	Holds all relevent files for disktra algorithm usage.
		hrUtils.py	Holds all required heuristic function, awa accessor to other modules.
		monteCarlo.py	Controller for simulations. Each heuristic is called through this modules init() method.

Running 
		Two ways:

		1. Run in terminal 
		   a) Open a terminal, navigate to the loaction of the file and change the permissions 
		      	     	       $ sudo chmod 755 main.py
		   b) In the same terminal, execute the code: 
		      	     	       $ ./main.py 
		
		2. Open terminal and run 
		   		       $ python2.7 main.py
		3. Opend terminal and run
		   	 	       $ python2.7 testMain.py 
				       
				       -> This is useful for diagnostics 
     
