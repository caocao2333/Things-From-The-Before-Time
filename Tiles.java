import java.awt.*;

public class Tiles {
	
	private boolean isShip;
	private boolean isSunk;
	private int tileType; //0: Water; 1: Carrier; 2: Battleship; 3: Cruiser; 4: Submarine; 5: Destroyer;
	private Color color;
	private int x;
	private int y;
	private int dir;//0: up; 1: down; 2: right; 3: left
	
	public Tiles(int xPos, int yPos){
		isShip = false;
		isSunk = false;
		tileType = 0;
		color = Color.CYAN;
		x = xPos;
		y = yPos;
	}
	
	public boolean checkIsShip() {
		return isShip;
	}
	
	public boolean checkIsSunk() {
		return isSunk;
	}
	
	public String getTileStat() {
		String[] returnValue = {"Water", "Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"};
		return returnValue[tileType];
	}
	
	public Color getTileColor() {
		return color;
	}

	public void placeShip(int shipType) {
		this.isShip = true;
		this.tileType = shipType;
		this.color = Color.GREEN;
	}
	
	public void sunkShip() {
		this.isSunk = true;
		this.color = Color.RED;
	}
	
	public void setDir(int direction) {
		this.dir = direction;
	}
	
	public String getDir() {
		if(dir == 0) {
			return "↑";
		}
		else if(dir == 1) {
			return "↓";
		}
		else if(dir == 2) {
			return "→";
		}
		else if(dir == 3) {
			return "←";
		}
		else {
			return "";
		}
	}
}
