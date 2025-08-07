import java.io.*;
import java.net.*;
import java.util.Date;

public class TimeServer {
    private ServerSocket serverSocket;

    public TimeServer(int port, int backlog) throws IOException {
        serverSocket = new ServerSocket(port, backlog);
        System.out.println("Time server is running on port " + port + "...");
    }

    public void serveForever() {
        while (true) {
            try (Socket clientSocket = serverSocket.accept()) {
                System.out.println("Connection from " + clientSocket.getInetAddress() + " has been established.");
                handleClient(clientSocket);
                System.out.println("Connection from " + clientSocket.getInetAddress() + " has been closed.");
            } catch (IOException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }

    private void handleClient(Socket clientSocket) {
        try {
            clientSocket.setSoTimeout(10000); // 10초 타임아웃
            InputStream in = clientSocket.getInputStream();
            OutputStream out = clientSocket.getOutputStream();

            byte[] buffer = new byte[1024];
            int read = in.read(buffer);
            String message = new String(buffer, 0, read);

            if ("GET TIME".equals(message.trim())) {
                System.out.println("클라이언트로부터 'GET TIME' 요청을 받았습니다.");
                String currentTime = new Date().toString();
                out.write(currentTime.getBytes());
            } else {
                System.out.println("알 수 없는 요청을 받았습니다.");
            }
        } catch (SocketTimeoutException e) {
            System.out.println("클라이언트 연결이 타임아웃되었습니다.");
        } catch (IOException e) {
            System.out.println("클라이언트 처리 중 오류: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws IOException {
        TimeServer server = new TimeServer(5000, 5);
        server.serveForever();
    }
}