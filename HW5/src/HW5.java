import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

public class HW5 extends JFrame {

    private JTextField priceField;
    private JTextField custIDField;
    private JTextField custNameField;
    private JTextField itemIDField;
    private JTextField itemNameField;
    private JTextField itemQuantityField;
    private Map<String, String> users; // Store username-password pairs

    private JTextField usernameField;
    private JPasswordField passwordField;


    public HW5() {
        setTitle("Sales Order Approval System");
        setSize(400, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(null);


        JLabel priceLabel = new JLabel("Price per unit:");
        priceLabel.setBounds(20, 20, 100, 20);
        add(priceLabel);

        JLabel custIDLabel = new JLabel("Customer ID:");
        custIDLabel.setBounds(20, 50, 100, 20);
        add(custIDLabel);

        custIDField = new JTextField();
        custIDField.setBounds(130, 50, 200, 20);
        add(custIDField);

        JLabel custNameLabel = new JLabel("Customer Name:");
        custNameLabel.setBounds(20, 80, 100, 20);
        add(custNameLabel);

        custNameField = new JTextField();
        custNameField.setBounds(130, 80, 200, 20);
        add(custNameField);

        JLabel itemIDLabel = new JLabel("Item ID:");
        itemIDLabel.setBounds(20, 110, 100, 20);
        add(itemIDLabel);

        itemIDField = new JTextField();
        itemIDField.setBounds(130, 110, 200, 20);
        add(itemIDField);

        JLabel itemNameLabel = new JLabel("Item Name:");
        itemNameLabel.setBounds(20, 140, 100, 20);
        add(itemNameLabel);

        itemNameField = new JTextField();
        itemNameField.setBounds(130, 140, 200, 20);
        add(itemNameField);

        JLabel itemQuantityLabel = new JLabel("Item Quantity:");
        itemQuantityLabel.setBounds(20, 170, 100, 20);
        add(itemQuantityLabel);

        itemQuantityField = new JTextField();
        itemQuantityField.setBounds(130, 170, 200, 20);
        add(itemQuantityField);

        priceField = new JTextField();
        priceField.setBounds(130, 20, 200, 20);
        add(priceField);


        // Other components...

        JButton submitButton = new JButton("Submit");
        submitButton.setBounds(100, 220, 100, 30);
        submitButton.addActionListener(e -> submitButtonClicked());
        add(submitButton);

        JButton deleteButton = new JButton("Delete");
        deleteButton.setBounds(220, 220, 100, 30);
        deleteButton.addActionListener(e -> deleteButtonClicked());
        add(deleteButton);

        setVisible(true);
    }

    private void submitButtonClicked() {
        double pricePerUnit = Double.parseDouble(priceField.getText());
        int custID = Integer.parseInt(custIDField.getText());
        String custName = custNameField.getText();
        int itemID = Integer.parseInt(itemIDField.getText());
        String itemName = itemNameField.getText();
        int itemQuantity = Integer.parseInt(itemQuantityField.getText());

        // Call your logic to submit the requisition

        // Display message dialog
        JOptionPane.showMessageDialog(this, "Sales requisition sent for approval", "Success", JOptionPane.INFORMATION_MESSAGE);
    }

    private void deleteButtonClicked() {
        // Call your logic to delete the requisition
        System.out.println("Deleting sales requisition...");
    }

    /*public static void main(String[] args) {
        SwingUtilities.invokeLater(HW5::new);
    }*/
}