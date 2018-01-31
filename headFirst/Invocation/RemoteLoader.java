package headFirst.Invocation;

public class RemoteLoader {
    public static void main(String[] args) {
        RemoteControl remoteControl = new RemoteControl();

        Light livingRoomLight = new Light("Living Room");
        Light KitchenLight = new Light("Kitchen");

        GarageDoor garageDoor = new GarageDoor();
        Stereo stereo = new Stereo();

        LightOnCommand livingRoomLightOnCommand = new LightOnCommand(livingRoomLight);
        LightOffCommand livingRoomLightOffCommand = new LightOffCommand(livingRoomLight);
        LightOnCommand kitchenLightOnCommand = new LightOnCommand(KitchenLight);
        LightOffCommand kitchenLightOffCommand = new LightOffCommand(KitchenLight);

        GarageDoorOpenCommand garageDoorOpenCommand = new GarageDoorOpenCommand(garageDoor);
        GarageDoorDownCommand garageDoorDownCommand = new GarageDoorDownCommand(garageDoor);

        StereoOnWithCDCommand stereoOnWithCDCommand = new StereoOnWithCDCommand(stereo);
        StereoOffCommand stereoOffCommand = new StereoOffCommand(stereo);

        remoteControl.setOnCommands(0, livingRoomLightOnCommand, livingRoomLightOffCommand);
        remoteControl.setOnCommands(1, kitchenLightOnCommand, kitchenLightOffCommand);
        remoteControl.setOnCommands(2, garageDoorOpenCommand, garageDoorDownCommand);
        remoteControl.setOnCommands(3, stereoOnWithCDCommand, stereoOffCommand);

        System.out.println(remoteControl);

        remoteControl.onButtonWasPushed(0);
        remoteControl.offButtonWasPushed(0);

        remoteControl.onButtonWasPushed(1);
        remoteControl.offButtonWasPushed(1);

        remoteControl.onButtonWasPushed(2);
        remoteControl.offButtonWasPushed(2);

        remoteControl.onButtonWasPushed(3);
        remoteControl.offButtonWasPushed(3);

        System.out.println("--- Macro On ---");
        Command[] partyOn = {livingRoomLightOnCommand, kitchenLightOnCommand, stereoOnWithCDCommand};
        MacroCommand macroCommand = new MacroCommand(partyOn);
        remoteControl.setOnCommands(6, macroCommand, null);
        remoteControl.onButtonWasPushed(6);
    }
}
