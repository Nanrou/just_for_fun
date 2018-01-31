package headFirst.Collection;

import java.util.ArrayList;

public class MenuTestDrive {
    public static void main(String[] args) {
//        PancakeHouseMenu pancakeHouseMenu = new PancakeHouseMenu();
//        DinerMenu dinerMenu = new DinerMenu();
//        CoffeeMenu coffeeMenu = new CoffeeMenu();
//
//        ArrayList menus = new ArrayList();
//        menus.add(pancakeHouseMenu);
//        menus.add(dinerMenu);
//        menus.add(coffeeMenu);
//
//        Waitress waitress = new Waitress(menus);
//        waitress.printMenu();

        MenuComponent pancakeHouseMenu = new Menu("Pancake House", "Breakfast");
        MenuComponent dinerMenu = new Menu("Diner Menu", "Lunch");
        MenuComponent cafeMenu = new Menu("Cafe Menu", "Dinner");
        MenuComponent dessertMenu = new Menu("Dessert Menu", "Dessert of course");

        MenuComponent allMenu = new Menu("All Menus", "All Menus combined");

//        Waitress waitress = new Waitress(pancakeHouseMenu);
//        waitress.printMenu();
//        waitress.printVegetarianMenu();

        // 这里等于是完全重构了，不用之前定义的菜单类，而是全部重新从menu出发

        pancakeHouseMenu.add(new MenuItem("K&B's Breakfast", "egg and toast", true, 2.99));
        pancakeHouseMenu.add(new MenuItem("Pancake Breakfast", "egg and sausage", false, 2.99));
        pancakeHouseMenu.add(new MenuItem("Blueberries Pancake", "pancake", true, 3.49));
        pancakeHouseMenu.add(new MenuItem("Waffles", "waffles with strawberries", true, 3.59));

        dinerMenu.add(new MenuItem("Vegetarian BLT", "lettuce & tomato", true, 2.99));
        dinerMenu.add(new MenuItem("BLT", "bacon & tomato", false, 2.99));
        dinerMenu.add(new MenuItem("Soup", "soup of potato", false, 3.29));
        dinerMenu.add(new MenuItem("HotDog", "hot dog with relish", false, 3.00));

        cafeMenu.add(new MenuItem("Burger", "Veggie burger", true, 3.99));
        cafeMenu.add(new MenuItem("Soup", "a cup of soup", false, 3.69));
        cafeMenu.add(new MenuItem("Burrito", "A large burrito", true, 4.39));


        allMenu.add(pancakeHouseMenu);
        allMenu.add(dinerMenu);
        allMenu.add(cafeMenu);

        dinerMenu.add(new MenuItem(
                "Pasta",
                "A slice of sourdough bread",
                true,
                3.89
        ));

        dinerMenu.add(dessertMenu);

        dessertMenu.add(new MenuItem(
                "Apple Pie",
                "Flakey crust",
                true,
                1.59
        ));

        Waitress waitress = new Waitress(allMenu);
        waitress.printMenu();
        waitress.printVegetarianMenu();
    }
}
