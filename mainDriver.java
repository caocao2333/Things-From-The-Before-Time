import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class mainDriver {
	public static JFrame mainWindow = new JFrame();
	public static Tiles[][][] gameBoard = new Tiles[2][10][10]; //Stacked game board, layer 0 is for player and layer 1 is for AI.;
	public static JButton[][] buttonMap = new JButton[10][10];
	public static Container container;
	public static GridBagConstraints c;
	public static boolean[] shipPlaced = new boolean[5];
	public static int[] shipLength = {5, 4, 3, 3, 2};
	public static int selectedX = -1;
	public static int selectedY = -1;
	public static String prompt;
	public static int counter = 0;
	
	public static void main(String[] args) {
		for(int i = 0; i < 10; i++) {
			for(int a = 0; a < 10; a++) {
				gameBoard[0][i][a] = new Tiles(a, i);
			}
		}
		setFrame();
		prompt = "Please select a tile to place your ship, or click \"skip\" to skip for now.";
		refreshButton();
	}
	
	public static void setFrame() {
		mainWindow.setSize(700,600);
		mainWindow.setTitle("Board");
		mainWindow.setResizable(false);
		mainWindow.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		container = mainWindow.getContentPane();
		mainWindow.setLayout(new GridBagLayout());
		c = new GridBagConstraints();
		c.fill = GridBagConstraints.BOTH;
		c.gridwidth = 1;
		c.weightx = 1;
		c.weighty = 1;
	}
	
	public static void refreshButton() {
		container.removeAll();
		for(int k = 0; k < 10; k++) {
			String yLb = "ABCDEFGHIJ";
			c.gridx = 0;
			c.gridy = k + 1;
			JLabel temp2 = new JLabel(Character.toString(yLb.charAt(k)));
			temp2.setHorizontalAlignment(JLabel.CENTER);
			container.add(temp2, c);
			c.gridx = k + 1;
			c.gridy = 0;
			JLabel temp = new JLabel(Integer.toString(k));
			temp.setHorizontalAlignment(JLabel.CENTER);
			container.add(temp, c);
		}
		for(int i = 0; i < 10; i++) {
			c.gridx = i + 1;
			for(int f = 0; f < 10; f++) {
				c.gridy = f + 1;
				buttonMap[i][f] = new JButton();
				buttonMap[i][f].setOpaque(false);
				buttonMap[i][f].setBackground((gameBoard[0][i][f].getTileColor()));
				buttonMap[i][f].addActionListener(new ALBoard());
	            buttonMap[i][f].putClientProperty("column", i);
	            buttonMap[i][f].putClientProperty("row", f);
	            container.add(buttonMap[i][f], c);
	            buttonMap[i][f].setOpaque(true);
			}
		}
		
		c.gridwidth = 3;
		c.gridx = 11;
		c.gridy = 11;
		JButton skip = new JButton();
		skip.setText("Skip");
		skip.setHorizontalAlignment(JLabel.CENTER);
		skip.addActionListener(new ALSkip());
		container.add(skip, c);
		c.gridy = 1;
		JLabel currentShip = new JLabel("Current Ship:");
		currentShip.setHorizontalAlignment(JLabel.CENTER);
		container.add(currentShip, c);
		c.gridwidth = 10;
		c.gridy = 11;
		c.gridx = 1;
		JLabel message = new JLabel(prompt);
		container.add(message, c);
		c.gridwidth = 1;
		mainWindow.setVisible(true);
	}
	
	public static void placeShip() {
		boolean[] dir = new boolean[4];//Up, Down, Left, Right
		//System.out.println(counter);
		if(selectedX >= 0) {
			if(selectedX + shipLength[counter] <= 10) {
				//can go right
				boolean haveShip = false;
				for(int i = 0; i < shipLength[counter]; i++) {
					if(gameBoard[0][selectedX + i][selectedY].checkIsShip()) {
						haveShip = true;
					}
				}
				if(!haveShip) {
					dir[3] = true;
					//code below for place ship
					for(int q = 0; q < shipLength[counter]; q++) {
						gameBoard[0][selectedX + q][selectedY].placeShip(0);
						shipPlaced[counter] = true;
					}
					if(counter >= 4) {
						counter = 0;
					}
					else {
						counter++;
					}
				}
			}
			System.out.println(Arrays.toString(shipPlaced));
			if(selectedX - shipLength[counter] >= 0) {
				//can go left
				boolean haveShip = false;
				for(int i = 0; i < shipLength[counter]; i++) {
					if(gameBoard[0][selectedX - i][selectedY].checkIsShip()) {
						haveShip = true;
					}
				}
				if(!haveShip) {
					dir[2] = true;
					//move ship
					for(int q = 0; q < shipLength[counter]; q++) {
						gameBoard[0][selectedX - q][selectedY].placeShip(0);
						shipPlaced[counter] = true;
					}
					if(counter >= 4) {
						counter = 0;
					}
					else {
						counter++;
					}
				}
			}
			if(selectedY + shipLength[counter] <= 10) {
				//can go down
				boolean haveShip = false;
				for(int i = 0; i < shipLength[counter]; i++) {
					if(gameBoard[0][selectedX][selectedY + i].checkIsShip()) {
						haveShip = true;
					}
				}
				if(!haveShip) {
					dir[1] = true;
					//move ship
					for(int q = 0; q < shipLength[counter]; q++) {
						gameBoard[0][selectedX][selectedY + q].placeShip(0);
						shipPlaced[counter] = true;
					}
					if(counter >= 4) {
						counter = 0;
					}
					else {
						counter++;
					}
				}
			}
			if(selectedY - shipLength[counter] >= 0) {
				//can go up
				boolean haveShip = false;
				for(int i = 0; i < shipLength[counter]; i++) {
					if(gameBoard[0][selectedX][selectedY - i].checkIsShip()) {
						haveShip = true;
					}
				}
				if(!haveShip) {
					dir[0] = true;
					//move ship
					for(int q = 0; q < shipLength[counter]; q++) {
						gameBoard[0][selectedX][selectedY - q].placeShip(0);
						shipPlaced[counter] = true;
					}
					if(counter >= 4) {
						counter = 0;
					}
					else {
						counter++;
					}
				}
			}
			refreshButton();
		}
	}
}

class ALBoard implements ActionListener {

	@Override
	public void actionPerformed(ActionEvent e) {
		if(!(mainDriver.shipPlaced[0] && mainDriver.shipPlaced[1] && mainDriver.shipPlaced[2] && mainDriver.shipPlaced[3] && mainDriver.shipPlaced[4])) {
			String yLb = "ABCDEFGHIJ";
			JButton btn = (JButton) e.getSource();
			mainDriver.selectedX = (int)btn.getClientProperty("column");
			mainDriver.selectedY = (int)btn.getClientProperty("row");
			System.out.println(mainDriver.selectedX + ", " + mainDriver.selectedY);
			mainDriver.placeShip();
			//mainDriver.gameBoard[0][mainDriver.selectedX][mainDriver.selectedY].sunkShip();
			mainDriver.refreshButton();
			System.out.println(yLb.charAt(mainDriver.selectedY) + "" + mainDriver.selectedX);
		}
	}
}

class ALSkip implements ActionListener {
	
	@Override
	public void actionPerformed(ActionEvent e) {
		//String yLb = "ABCDEFGHIJ";
		JButton btn = (JButton) e.getSource();
		if(!(mainDriver.shipPlaced[0] && mainDriver.shipPlaced[1] && mainDriver.shipPlaced[2] && mainDriver.shipPlaced[3] && mainDriver.shipPlaced[4])) {
			if(mainDriver.counter <= 4 && mainDriver.shipPlaced[mainDriver.counter] == false) {
				mainDriver.placeShip();
			}
			if(mainDriver.counter >= 4) {
				mainDriver.counter = 0;
			}
			else {
				mainDriver.counter++;
			}
		}
		//System.out.println(yLb.charAt((int)btn.getClientProperty("column")) + "" + btn.getClientProperty("row"));
	}
}
