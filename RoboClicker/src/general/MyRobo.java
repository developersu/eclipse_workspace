package general;

import java.awt.AWTException;
import java.awt.Robot;


public class MyRobo {
	
	private int time;
	
	public void doIt() 
			throws AWTException {
		
		Robot ostap = new Robot();
		
		ostap.mouseMove(500, 600);
		ostap.delay(500);
		ostap.mousePress(1);
	}
}
