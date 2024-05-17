#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <unistd.h>

#include <glog/logging.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <sys/epoll.h>
#include <arpa/inet.h>

#define LOCAL_PORT 8000

#define MAX_EVENTS 12

using namespace std;
using namespace google;

int epollFd;
struct epoll_event epollEvents[MAX_EVENTS];
struct epoll_event epollBuf;
int g_serverSocked;
int g_clientSocked;
char g_recvBuf[128] = {0};
char g_sendBuf[128] = {0};

int InitGoogleLogService(const char *argv0)
{
    google::InitGoogleLogging(argv0);
    FLAGS_logtostderr = 1;
    FLAGS_log_dir = "./log/";

    LOG(INFO) << "Init Google Log Service Success!"
              << " log_dir: " << FLAGS_log_dir;

    return 0;
}

int InitSockedService(void)
{
    int ret;

    g_serverSocked = socket(AF_INET, SOCK_STREAM, 0);
    if (g_serverSocked < 0)
    {
        LOG(ERROR) << "Create Socked Failed!";
        return g_serverSocked;
    }
    LOG(INFO) << "Create Socked Success!";

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(LOCAL_PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    bind(g_serverSocked, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
    LOG(INFO) << "Bind Socked Success!";

    ret = listen(g_serverSocked, 5);
    if (ret < 0)
    {
        LOG(ERROR) << "Listen Socked Failed!";
        return ret;
    }
    LOG(INFO) << "Listen Socked Success!";

    return 0;
}

int SockedConner(void)
{
    sockaddr_in clientAddr;
    socklen_t addrLen = sizeof(clientAddr);
    int clientSocked;
    clientSocked = accept(g_serverSocked, (struct sockaddr *)&clientAddr, &addrLen);
    if (clientSocked < 0)
    {
        LOG(ERROR) << "Accept Socked Failed!";
        return clientSocked;
    }
    LOG(INFO) << "Accept Socked Success!";

    return clientSocked;
}

int CreateEpoll(void)
{
    int ret;

    epollFd = epoll_create1(0);
    if (epollFd < 0)
    {
        LOG(ERROR) << "Create Epoll Failed!";
        return epollFd;
    }
    LOG(INFO) << "Create Epoll Success!";

    epollBuf.events = EPOLLIN;
    epollBuf.data.fd = g_serverSocked;
    ret = epoll_ctl(epollFd, EPOLL_CTL_ADD, g_serverSocked, &epollBuf);
    if (ret < 0)
    {
        LOG(ERROR) << "Epoll Ctl Add Failed!";
        return ret;
    }
    LOG(INFO) << "Epoll Ctl Add Success!";
    return 0;
}

int SockedMainService(int fd)
{
    memset(g_recvBuf, 0, sizeof(g_recvBuf));
    recv(fd, g_recvBuf, sizeof(g_recvBuf), 0);
    cout << "Recv: " << g_recvBuf << endl;
    if (strlen(g_recvBuf) < 0 || strlen(g_recvBuf) == 0)
    {
        LOG(ERROR) << "Client Disconnect!";
        return -2;
    }
    if (strcmp(g_recvBuf, "exit") == 0)
    {
        LOG(INFO) << "Client exit!";
        return -1;
    }

    memset(g_sendBuf, 0, sizeof(g_sendBuf));
    strcpy(g_sendBuf, "Hello, I'm Server!");
    send(fd, g_sendBuf, strlen(g_sendBuf), 0);
    cout << "Send: " << g_sendBuf << endl;

    return 0;
}

int main(int argc, char *argv[])
{
    int ret;

#ifdef NDEBUG
    LOG(INFO) << "Release Version!";
#else
    LOG(INFO) << "Debug Version!";
#endif

    if (InitGoogleLogService(argv[0]) != 0)
    {
        return EXIT_FAILURE;
    }
    if (InitSockedService() != 0)
    {
        return EXIT_FAILURE;
    }
    if (CreateEpoll() != 0)
    {
        return EXIT_FAILURE;
    }

    int nfds;
    while (1)
    {
        nfds = epoll_wait(epollFd, epollEvents, MAX_EVENTS, -1);
        if (nfds < 0)
        {
            LOG(ERROR) << "Epoll Wait Failed!";
            break;
        }
        for (int i = 0; i < nfds; i++)
        {
            if (epollEvents[i].data.fd == g_serverSocked)
            {
                LOG(INFO) << "Epoll Events - socket conner";
                int connectSocket = SockedConner();
                if (connectSocket < 0)
                {
                    continue;
                }
                epollBuf.events = EPOLLIN;
                epollBuf.data.fd = connectSocket;
                ret = epoll_ctl(epollFd, EPOLL_CTL_ADD, connectSocket, &epollBuf);
                if (ret < 0)
                {
                    LOG(ERROR) << "Epoll Ctl Add Failed!";
                    continue;
                }
                LOG(INFO) << "Epoll Ctl Add Success!";
            }
            else
            {
                LOG(INFO) << "Epoll Events - socket in service";
                if (SockedMainService(epollEvents[i].data.fd) < 0)
                {
                    ret = epoll_ctl(epollFd, EPOLL_CTL_DEL, epollEvents[i].data.fd, &epollEvents[i]);
                    if (ret < 0)
                    {
                        LOG(ERROR) << "Epoll Ctl Del Failed!";
                    }
                    close(epollEvents[i].data.fd);
                    LOG(INFO) << "Close Client Socked!";
                }
            }
        }
    }

    close(g_clientSocked);
    LOG(INFO) << "Close Client Socked!";

    return EXIT_SUCCESS;
}