from mfrc522 import MFRC522
from machine import Pin
import time
from keypad import Keypad

pino_sck = 18
pino_mosi = 23
pino_miso = 19
pino_cs = 5
pino_rst = 22

combos_spi_baud = [(1, 500000), (1, 250000), (2, 500000), (2, 250000)]

leitor_rfid = None
configuracao_usada = None

for spi_id, baud in combos_spi_baud:
    try:
        leitor = MFRC522(sck=pino_sck, mosi=pino_mosi, miso=pino_miso,
                         sda=pino_cs, rst=pino_rst, spi_id=spi_id, baudrate=baud, reset_delay=120)
        try:
            versao = leitor._read_reg(0x37)
        except:
            versao = None
        if versao is not None:
            leitor_rfid = leitor
            configuracao_usada = (spi_id, baud, versao)
            break
    except:
        time.sleep_ms(100)

if leitor_rfid is None:
    raise SystemExit("Falha na inicialização do RFID.")

def uid_para_string(uid):
    return ":".join("{:02X}".format(x) for x in uid)

pinos_linhas_teclado = [32, 33, 25, 26]
pinos_colunas_teclado = [27, 14, 12]

mapa_teclas = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

teclado = Keypad(pinos_linhas_teclado, pinos_colunas_teclado, mapa_teclas)

led_always_on = Pin(2, Pin.OUT)
led_blink = Pin(4, Pin.OUT)

led_always_on.value(1)

ultimo_uid = None

try:
    while True:
        acionou_led = False

        sucesso, bits = leitor_rfid.request()
        if sucesso:
            uid = leitor_rfid.anticoll()
            if uid:
                uid_str = uid_para_string(uid)
                if uid_str != ultimo_uid:
                    print("Cartão detectado — UID:", uid_str)
                    ultimo_uid = uid_str
                    acionou_led = True
            else:
                print("Request OK, anticoll falhou")
        else:
            if ultimo_uid is not None:
                print("Cartão removido")
                ultimo_uid = None

        tecla = teclado.scan()
        if tecla and tecla in '0123456789*#':
            print("Tecla pressionada:", tecla)
            acionou_led = True

        if acionou_led:
            led_blink.value(1)
            time.sleep_ms(150)
            led_blink.value(0)

        time.sleep_ms(80)

except KeyboardInterrupt:
    print("Interrompido pelo usuário.")
except Exception as erro:
    print("Erro:", erro)

