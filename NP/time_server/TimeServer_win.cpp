#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

#include <iostream>
#include <string>
#include <ctime>

class TimeServer {
private:
#ifdef _WIN32
    SOCKET server_sock;
#else
    int server_sock;
#endif
    int port;
    int backlog;
public:
    TimeServer(int port = 5000, int backlog = 5) : port(port), backlog(backlog) {
#ifdef _WIN32
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2,2), &wsaData);
#endif
        server_sock = socket(AF_INET, SOCK_STREAM, 0);
        if (
#ifdef _WIN32
            server_sock == INVALID_SOCKET
#else
            server_sock < 0
#endif
        ) {
            std::cerr << "소켓 생성 실패\n";
            exit(1);
        }
        sockaddr_in addr = {};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        int opt = 1;
        setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (char*)&opt, sizeof(opt));
        if (bind(server_sock, (sockaddr*)&addr, sizeof(addr)) < 0) {
            std::cerr << "바인드 실패\n";
#ifdef _WIN32
            closesocket(server_sock);
            WSACleanup();
#else
            close(server_sock);
#endif
            exit(1);
        }
        if (listen(server_sock, backlog) < 0) {
            std::cerr << "리스닝 실패\n";
#ifdef _WIN32
            closesocket(server_sock);
            WSACleanup();
#else
            close(server_sock);
#endif
            exit(1);
        }
        std::cout << "Time server is running on port " << port << "..." << std::endl;
    }

    void serveForever() {
        while (true) {
            sockaddr_in client_addr;
#ifdef _WIN32
            int addrlen = sizeof(client_addr);
#else
            socklen_t addrlen = sizeof(client_addr);
#endif
            auto client_sock = accept(server_sock, (sockaddr*)&client_addr, &addrlen);
            if (
#ifdef _WIN32
                client_sock == INVALID_SOCKET
#else
                client_sock < 0
#endif
            ) {
                std::cerr << "클라이언트 연결 실패\n";
                continue;
            }
            std::cout << "Connection from " << inet_ntoa(client_addr.sin_addr) << " has been established." << std::endl;
            handleClient(client_sock);
#ifdef _WIN32
            closesocket(client_sock);
#else
            close(client_sock);
#endif
            std::cout << "Connection closed." << std::endl;
        }
    }

    void handleClient(
#ifdef _WIN32
        SOCKET client_sock
#else
        int client_sock
#endif
    ) {
        char buffer[1024] = {0};
        int bytes = recv(client_sock, buffer, sizeof(buffer)-1, 0);
        if (bytes <= 0) {
            std::cout << "클라이언트로부터 데이터를 받지 못했습니다." << std::endl;
            return;
        }
        buffer[bytes] = '\0';
        std::string message(buffer);
        if (message == "GET TIME") {
            std::cout << "클라이언트로부터 'GET TIME' 요청을 받았습니다." << std::endl;
            std::time_t now = std::time(nullptr);
            std::string current_time = std::ctime(&now);
            send(client_sock, current_time.c_str(), current_time.size(), 0);
        } else {
            std::cout << "알 수 없는 요청을 받았습니다." << std::endl;
        }
    }

    void closeServer() {
#ifdef _WIN32
        closesocket(server_sock);
        WSACleanup();
#else
        close(server_sock);
#endif
        std::cout << "서버 소켓이 닫힙니다." << std::endl;
    }
};

int main() {
    TimeServer server(5000, 5);
    server.serveForever();
    server.closeServer();
    return 0;
}
