package headFirst.Collection;

import java.util.Iterator;

public class DinerMenu extends Menu {
    static final int MAX_ITEMS = 6;
    int numberOfItems = 0;
    MenuItem[] menuItems;

    public DinerMenu(String name, String description) {
        super(name, description);

        menuItems = new MenuItem[MAX_ITEMS];

        addItem("Vegetarian BLT", "lettuce & tomato", true, 2.99);
        addItem("BLT", "bacon & tomato", false, 2.99);
        addItem("Soup", "soup of potato", false, 3.29);
        addItem("HotDog", "hot dog with relish", false, 3.00);

    }

    public void addItem(String name, String description,
                        boolean vegetarian, double price) {
        MenuItem menuItem = new MenuItem(name, description, vegetarian, price);
        if (numberOfItems >= MAX_ITEMS) {
            System.err.println("Sorry, menu is full!");
        } else {
            menuItems[numberOfItems] = menuItem;
            numberOfItems += 1;
        }
    }

    public Iterator createIterator() {
        return new DinerMenuIterator(menuItems);
    }
}
