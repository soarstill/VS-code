import java.io.*;
import java.net.*;

public class TimeClient {
    private Socket socket;

    public TimeClient(String host, int port) throws IOException {
        socket = new Socket(host, port);
        System.out.println("서버에 연결되었습니다.");
    }

    public void getTime() {
        try {
            OutputStream out = socket.getOutputStream();
            InputStream in = socket.getInputStream();

            out.write("GET TIME".getBytes());
            out.flush();

            byte[] buffer = new byte[1024];
            int read = in.read(buffer);
            if (read == -1) {
                System.out.println("서버로부터 응답을 받지 못했습니다.");
                return;
            }
            String currentTime = new String(buffer, 0, read);
            System.out.println("현재시각: " + currentTime);
        } catch (IOException e) {
            System.out.println("오류: " + e.getMessage());
        }
    }

    public void close() {
        try {
            socket.close();
            System.out.println("클라이언트 소켓이 닫힙니다.");
        } catch (IOException e) {
            System.out.println("소켓 닫기 오류: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        TimeClient client = new TimeClient("localhost", 5000);
        for (int i = 0; i < 5; i++) {
            client.getTime();
            Thread.sleep(3000); // 3초 대기
        }
        client.close();
    }
}
