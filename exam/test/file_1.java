class Point2d {
    /* The X and Y coordinates of the point--instance variables */
    private double x;
    private double y;
    private boolean debug;	// A trick to help with debugging

    public Point2d (double px, double py) { // Constructor
	x = px;
	y = py;

	debug = false;		// turn off debugging
    }

    public Point2d () {		// Default constructor
	this (0.0, 0.0);        // Invokes 2 parameter Point2D constructor
    }
    // Note that a this() invocation must be the BEGINNING of
    // statement body of constructor

    public Point2d (Point2d pt) {	// Another consructor
	x = pt.getX();
	y = pt.getY();

	// a better method would be to replace the above code with
	//    this (pt.getX(), pt.getY());
	// especially since the above code does not initialize the
	// variable debug.  This way we are reusing code that is already
	// working.
    }
}
