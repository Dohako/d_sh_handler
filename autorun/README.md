# Важно

Чтобы скрипт работал постоянное необходимо
в командном окне
на raspberry ввести `sudo nano /etc/rc.local`
и добавить внутрь этого документа строку

`su -c "/home/pi/d_sh_handler/autorun/repo_watcher/git-repo-watcher -d "/home/pi/d_sh_handler"" pi &`
`su -c "python3 /path/to/file.py" pi &`

Предлагаемый скрипт позволит системе
постоянно запускать главный
модуль программы.

В прошлой версии была организация запуска внутреннего
скрипта через строку
`/home/pi/d_sh_handler/bin/script_auto_run`,
что запускает проект не под текущим юзером.
Это приводит
к проблемам с библиотеками и
периферийными устройствами.
