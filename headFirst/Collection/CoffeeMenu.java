package headFirst.Collection;

import java.util.Hashtable;
import java.util.Iterator;

public class CoffeeMenu extends Menu {  // 这里没有必要继承，因为已经放弃这里了
    Hashtable menuItems = new Hashtable();

    public CoffeeMenu(String name, String description) {
        super(name, description);

        addItem("Burger", "Veggie burger", true, 3.99);
        addItem("Soup", "a cup of soup", false, 3.69);
        addItem("Burrito", "A large burrito", true, 4.39);

    }

    public void addItem(String name, String description,
                        boolean vegetarian, double price) {
        MenuItem menuItem = new MenuItem(name, description, vegetarian, price);
        menuItems.put(menuItem.getName(), menuItem);
    }

    @Override
    public Iterator createIterator() {
        return menuItems.values().iterator();
    }
}
