package general;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.FlowLayout;

import javax.swing.JFrame;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import javax.swing.JPanel;
import java.awt.GridBagConstraints;
import javax.swing.JButton;
import javax.swing.JTable;
import javax.swing.JToolBar;
import javax.swing.SwingConstants;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import java.awt.Component;
import javax.swing.JLabel;

public class MainWindow {

	private JFrame frame;
	private JTable table;
	
	private void set_button_to_panel(JButton x, JToolBar panel){
		Box.Filler box_separator = new Box.Filler(new Dimension(60, 5), new Dimension(60, 5), new Dimension(60, 5));
		box_separator.setAlignmentX(Component.CENTER_ALIGNMENT);
		panel.add(box_separator);
		
		x.setPreferredSize(new Dimension(50, 50));
		x.setMinimumSize(new Dimension(50, 50));
		x.setMaximumSize(new Dimension(50, 50));
		x.setSize(new Dimension(50, 50));
		x.setBackground(new Color(239, 240, 241));
		x.setContentAreaFilled(true);
		x.setAlignmentX(Component.CENTER_ALIGNMENT);
		panel.add(x);
	}

	/* Launch the application. */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainWindow window = new MainWindow();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/* Create the application. */
	public MainWindow() {
		initialize();
	}

	/* Initialize the contents of the frame. */
	private void initialize() {
		frame = new JFrame("Loper's robot");
		frame.setBounds(100, 100, 1200, 900);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setLocationRelativeTo(null);
		
		GridBagLayout gridBagLayout = new GridBagLayout();
		gridBagLayout.columnWidths = new int[]{0, 0, 0};
		gridBagLayout.rowHeights = new int[]{0, 0};
		gridBagLayout.columnWeights = new double[]{0.0, 1.0, Double.MIN_VALUE};
		gridBagLayout.rowWeights = new double[]{0.0, Double.MIN_VALUE};
		frame.getContentPane().setLayout(gridBagLayout);
		
		
		JToolBar panel = new JToolBar();
		panel.setFloatable(false);
		panel.setOrientation(JToolBar.VERTICAL);
		panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
		panel.setBackground(new Color(245, 252, 255));

		frame.getContentPane().add(panel, new GridBagConstraints(0,0,1,2,0.0f,0.0f,GridBagConstraints.FIRST_LINE_START, GridBagConstraints.VERTICAL, new Insets(0, 0, 0, 5), 0, 0));
		
		// * Add buttons to the panel
		JButton btn_rec = new JButton("", new ImageIcon(MainWindow.class.getResource("/img/rec.png")));
		this.set_button_to_panel(btn_rec, panel);

		JButton btn_play = new JButton("", new ImageIcon(MainWindow.class.getResource("/img/play.png")));
		this.set_button_to_panel(btn_play, panel);
		
		JButton btn_save = new JButton("", new ImageIcon(MainWindow.class.getResource("/img/save.png")));
		this.set_button_to_panel(btn_save, panel);
		
		JButton btn_load = new JButton("", new ImageIcon(MainWindow.class.getResource("/img/load.png")));
		this.set_button_to_panel(btn_load, panel);		

		
		table = new JTable(40, 8);
		frame.getContentPane().add(table, new GridBagConstraints(1,1,1,1,1.0f,1.0f,GridBagConstraints.PAGE_START, GridBagConstraints.BOTH, new Insets(10, 0, 0, 5), 0, 0));
		
		JLabel lblEvents = new JLabel("Events List");
		
		GridBagConstraints gbc_lblNewLabel = new GridBagConstraints();
		gbc_lblNewLabel.anchor = GridBagConstraints.WEST;
		gbc_lblNewLabel.insets = new Insets(0, 0, 0, 0);
		gbc_lblNewLabel.gridx = 1;
		gbc_lblNewLabel.gridy = 0;
		frame.getContentPane().add(lblEvents, gbc_lblNewLabel);
		

		
	}

}
