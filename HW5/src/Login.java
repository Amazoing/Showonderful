import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

public class Login extends JFrame {

    private Map<String, String> users; // Store username-password pairs

    private JTextField usernameField;
    private JPasswordField passwordField;

    public Login() {
        setTitle("Login");
        setSize(400, 200);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(3, 2));

        JLabel usernameLabel = new JLabel("Username:");
        add(usernameLabel);

        usernameField = new JTextField();
        add(usernameField);

        JLabel passwordLabel = new JLabel("Password:");
        add(passwordLabel);

        passwordField = new JPasswordField();
        add(passwordField);

        JButton loginButton = new JButton("Login");
        loginButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loginButtonClicked();
            }
        });
        add(loginButton);

        users = new HashMap<>();
        users.put("testuser", "test123");

        setVisible(true);
    }

    private void loginButtonClicked() {
        String username = usernameField.getText();
        String password = new String(passwordField.getPassword());

        if (users.containsKey(username) && users.get(username).equals(password)) {
            openSalesOrderForm();
        } else {
            JOptionPane.showMessageDialog(this, "Invalid username or password", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void openSalesOrderForm() {
        // Open the sales order requisition form
        SwingUtilities.invokeLater(() -> {
            HW5 salesOrderApprovalGUI = new HW5();
            salesOrderApprovalGUI.setVisible(true);
            dispose(); // Close the login window
        });
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Login::new);
    }
}

