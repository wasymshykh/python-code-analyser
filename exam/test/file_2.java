class Point2d {
   
    public void setXY(double px, double py) {
	setX(px);
	setY(py);
    }

    public double distanceFrom (Point2d pt) {
	double dx = Math.abs(x - pt.getX());
	double dy = Math.abs(y - pt.getY());

	// check out the use of dprint()
	dprint ("distanceFrom(): deltaX = " + dx);
	dprint ("distanceFrom(): deltaY = " + dy);

	return Math.sqrt((dx * dx) + (dy * dy));
    }

    public double distanceFromOrigin () {
	return distanceFrom (new Point2d ( ));
    }

    public String toStringForXY() {
	String str = "(" + x + ", " + y;
	return str;
    }

    public String toString() {
	String str = toStringForXY() + ")";
	return str;
    }
}
