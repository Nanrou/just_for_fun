package headFirst.Collection;

import java.util.ArrayList;
import java.util.Iterator;

public class PancakeHouseMenu extends Menu {
    ArrayList menuItems;
//    MenuComponent menuItems;
    
    public PancakeHouseMenu(String name, String description) {
        super(name, description);
        menuItems = new ArrayList();

        addItem("K&B's Breakfast", "egg and toast", true, 2.99);
        addItem("Pancake Breakfast", "egg and sausage", false, 2.99);
        addItem("Blueberries Pancake", "pancake", true, 3.49);
        addItem("Waffles", "waffles with strawberries", true, 3.59);
    }

    public void addItem(String name, String description,
                    boolean vegetarian, double price) {
        MenuItem menuItem = new MenuItem(name, description, vegetarian, price);
        menuItems.add(menuItem);
    }

    public Iterator createIterator()
    {
        return menuItems.iterator();
    }

}
