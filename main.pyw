import subprocess;
import tkinter;
import os;
import threading;

def getNetworkInformation(pingMeter, canvas):

    global running;
    #gatewayAddressProcess = subprocess.Popen(["ipconfig"], shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin = subprocess.PIPE, cwd = os.getcwd(), env = os.environ);
    #gatewayAddressProcess.stdin.close();
    #gatewayAddress = gatewayAddressProcess.stdout.read().decode("utf-8").strip()[-32:].strip();
    gatewayAddress = "8.8.8.8"
    networkData = [];
    networkDataRawBuffer = [];
    while running:
        pingShell = subprocess.Popen(["ping", "-w", "1000", "-n", "20", gatewayAddress], shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE, cwd = os.getcwd(), env = os.environ);
        pingShell.stdin.close();
        while running:
            if pingShell.poll() == 0:
                break;
            else:
                pingShellLine = pingShell.stdout.readline().decode("utf-8").strip();
                if ("Reply from " in pingShellLine) or (pingShellLine == "Request timed out."):
                    if "Reply from " in pingShellLine:
                        networkDataRawBuffer.append(int(pingShellLine[pingShellLine.index("time") + 5:pingShellLine.find("ms")]));
                    elif pingShellLine == "Request timed out.":
                        networkDataRawBuffer.append(1000);
                    if len(networkDataRawBuffer) > 5:
                        networkDataRawBuffer.pop(0);
                    if len(networkDataRawBuffer) == 5:
                        networkData.append(round(sum(networkDataRawBuffer)/5));
                    if len(networkData) > 36:
                        networkData.pop(0);
                    if len(networkData) > 1 and running:
                        threading.Thread(target = drawNetworkInformation, args = (pingMeter, canvas, networkData)).start();
    pingShell.kill();

def drawNetworkInformation(pingMeter, canvas, networkData):

    global running;

    if running:
        pingMeter.config(text = "Current Ping: " + str(networkData[-1]) + " ms");
        canvas.create_rectangle(2, 0, 700, 698, fill = "#212121", outline = "");
        drawPoints = [(720 - (len(networkData) * 20)), 698];
        for i in range(len(networkData)):
            drawPoints.extend([720 - ((len(networkData) - i) * 20), 698 - round((698 * networkData[i])/1000)]);
        drawPoints.extend([700, 698]);
        if running:
            canvas.create_polygon(drawPoints, fill = "#175e64");    
            canvas.create_line(drawPoints[2:-2], fill = "#00eeff", width = 2);
            canvas.create_line(1, 0, 1, 700, fill = "#00eeff", width = 2);

def main():

    global running;
    running = True;

    root = tkinter.Tk();
    #root.wm_iconbitmap("icon.ico");
    root.config(bg = "#212121");
    root.title("Network Visualizer");
    root.geometry("800x800");
    root.resizable(False, False);
    
    canvas = tkinter.Canvas(root);
    canvas.config(bg = "#212121", bd = 0, highlightthickness = 0, relief = "ridge");
    canvas.place(x = 100, y = 0, width = 700, height = 700);
    canvas.create_line(1, 0, 1, 700, fill = "#00eeff", width = 2);
    canvas.create_line(0, 699, 700, 699, fill = "#00eeff", width = 2);

    yLabel = tkinter.Label(root, text = "Ping\n(ms)", font = ("Helvetica", 12), bg = "#212121", fg = "#00eeff");
    yLabel.place(x = 30, y = 325, width = 40, height = 50);

    xLabel = tkinter.Label(root, text = "Time", font = ("Helvetica", 12), bg = "#212121", fg = "#00eeff");
    xLabel.place(x = 430, y = 735, width = 40, height = 30);

    pingMeter = tkinter.Label(root, text = "Current Ping: N/A", font = ("Helvetica", 12), bg = "#212121", fg = "#00eeff");
    pingMeter.place(x = 20, y = 735, width = 180, height = 30);

    networkThread = threading.Thread(target = getNetworkInformation, args = (pingMeter, canvas));
    networkThread.start();

    root.mainloop();
    root.quit();
    
    running = False;

main();
