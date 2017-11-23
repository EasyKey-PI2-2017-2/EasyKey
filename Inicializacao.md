
O ambiente de inicialização deve primeiramente executar o servidor Django sendo
que logo em seguida deverá abrir uma janela do Google Chrome em tela inteira, no
endereço especificado.

Abra para edição o arquivo rc.local, com o comando:

sudo nano /etc/rc.local

Adicionar ao final do arquivo a execução do servidor

python manage.py runserver localhost:8080 &

Adicionar linha que abre o Google Chrome, nessa linha além de navegação anônima,
existem parâmetros para que os campos digitáveis não fiquem na cache.

google-chrome --chrome --kiosk --start-fullscreen http://localhost:8080 --incognito --disable-pinch --overscroll-history-navigation=0 -start-fullscreen
