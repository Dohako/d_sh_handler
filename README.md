# Dohako smart home handler

Made for raspberry pi.

This is my software to constantly update and keep running some programms. Also this soft will reboot device every n time.

____

Данный репозиторий создан для постоянного поддержания актуальности софта на моей Raspberry PI. Предполагается, что так будет проще обновлять и запускать скрипты, которые требуют собственного потока

## Known errors

1. `ImportError: libcblas.so.3: cannot open shared object file: No such file or directory`

*Solution*:
sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test
