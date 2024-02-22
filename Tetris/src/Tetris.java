import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

public class Tetris {

    private static final int ROWS = 20;
    private static final int COLS = 10;
    private static final char EMPTY = ' ';
    private static final char BLOCK = '#';

    private char[][] board;
    private int currentRow, currentCol;
    private int[][] currentShape;
    private int score;

    public Tetris() {
        board = new char[ROWS][COLS];
        currentRow = 0;
        currentCol = COLS / 2 - 1;
        score = 0;
        initBoard();
        newShape();
    }

    private void initBoard() {
        for (char[] row : board) {
            Arrays.fill(row, EMPTY);
        }
    }

    private void newShape() {
        Random random = new Random();
        int shapeIndex = random.nextInt(Shapes.SHAPES.length);
        currentShape = Shapes.SHAPES[shapeIndex];
        currentRow = 0;
        currentCol = COLS / 2 - 1;
        if (isCollision()) {
            gameOver();
        }
    }

    private boolean isCollision() {
        for (int i = 0; i < currentShape.length; i++) {
            for (int j = 0; j < currentShape[i].length; j++) {
                if (currentShape[i][j] == 1 &&
                        (currentRow + i >= ROWS || currentCol + j < 0 || currentCol + j >= COLS || board[currentRow + i][currentCol + j] == BLOCK)) {
                    return true;
                }
            }
        }
        return false;
    }

    private void mergeShape() {
        for (int i = 0; i < currentShape.length; i++) {
            for (int j = 0; j < currentShape[i].length; j++) {
                if (currentShape[i][j] == 1) {
                    board[currentRow + i][currentCol + j] = BLOCK;
                }
            }
        }
    }

    private void clearLines() {
        for (int i = ROWS - 1; i >= 0; i--) {
            boolean isFull = true;
            for (int j = 0; j < COLS; j++) {
                if (board[i][j] == EMPTY) {
                    isFull = false;
                    break;
                }
            }
            if (isFull) {
                // Remove the full line and shift above lines down
                for (int k = i; k > 0; k--) {
                    System.arraycopy(board[k - 1], 0, board[k], 0, COLS);
                }
                score++;
            }
        }
    }

    private void printBoard() {
        for (char[] row : board) {
            for (char cell : row) {
                System.out.print(cell);
            }
            System.out.println();
        }
        System.out.println("Score: " + score);
    }

    private void gameOver() {
        System.out.println("Game Over! Your Score: " + score);
        System.exit(0);
    }

    private void moveDown() {
        currentRow++;
        if (isCollision()) {
            currentRow--;
            mergeShape();
            clearLines();
            newShape();
        }
    }

    private void moveLeft() {
        currentCol--;
        if (isCollision()) {
            currentCol++;
        }
    }

    private void moveRight() {
        currentCol++;
        if (isCollision()) {
            currentCol--;
        }
    }

    private void rotate() {
        int[][] temp = currentShape;
        currentShape = Shapes.rotate(currentShape);
        if (isCollision()) {
            currentShape = temp;
        }
    }

    public void run() {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            printBoard();
            System.out.print("Move (A/D/L/R, Q to quit): ");
            String input = scanner.next().toUpperCase();
            switch (input) {
                case "A":
                    moveLeft();
                    break;
                case "D":
                    moveRight();
                    break;
                case "L":
                    rotate();
                    break;
                case "R":
                    moveDown();
                    break;
                case "Q":
                    System.exit(0);
                    break;
            }
        }
    }

    public static void main(String[] args) {
        Tetris tetris = new Tetris();
        tetris.run();
    }
}

class Shapes {

    public static final int[][][] SHAPES = {
            // I
            {
                    {1, 1, 1, 1}
            },
            // J
            {
                    {1, 0, 0},
                    {1, 1, 1}
            },
            // L
            {
                    {0, 0, 1},
                    {1, 1, 1}
            },
            // O
            {
                    {1, 1},
                    {1, 1}
            },
            // S
            {
                    {0, 1, 1},
                    {1, 1, 0}
            },
            // T
            {
                    {0, 1, 0},
                    {1, 1, 1}
            },
            // Z
            {
                    {1, 1, 0},
                    {0, 1, 1}
            }
    };

    public static int[][] rotate(int[][] shape) {
        int rows = shape.length;
        int cols = shape[0].length;
        int[][] rotated = new int[cols][rows];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                rotated[j][rows - 1 - i] = shape[i][j];
            }
        }
        return rotated;
    }
}
