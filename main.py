from machine import Pin, ADC, I2C  # Raspberry Pi PicoでA-D変換、I2Cを使用するためのモジュールをインポート
from ssd1306 import SSD1306_I2C  # 有機ELディスプレイを使用するためのモジュールをインポート
import math  # 対数の計算をするためのモジュールをインポート
import time  # 時間に関する関数を取り扱うためのモジュールをインポート

B = 3435  # B定数 [K]
T_a = 25.0 + 273.15  # サーミスタの基準温度 [K]
R_a = 10.0  # サーミスタの基準温度での電気抵抗 [kΩ]

R_1 = 10.0  # 固定抵抗器の電気抵抗 [kΩ]

interval = 2.0  # 測定値を表示する時間間隔 [秒]
sample = 20  # 測定値を表示する間の測定回数 [回]

thermistor = ADC(Pin(26))  # 26番ピンを指定してADCオブジェクトを作成

i2c = I2C(1, sda=Pin(14), scl=Pin(15))  # I2Cで接続する有機ELディスプレイのSDAを14番、SCLを15番ピンに指定してI2Cペリフェラルを作成
oled = SSD1306_I2C(128, 64, i2c)  # 有機ELディスプレイの解像度を128px*64pxと設定
oled.fill(0)  # ディスプレイを黒で塗りつぶし


while True:  # 電源が入っている限りループ処理を継続
    n = 0  # ADCで読み取った値を代入する変数
    for _ in range(sample):  # sampleで指定した測定回数だけループ処理を継続
        n += thermistor.read_u16()  # 変数nにADCで読み取った値を足し合わせる
        time.sleep(interval / sample)  # intervalをsampleで割った秒数だけ待機、intervalが2.0秒、sampleが20回だと0.1秒待機
    n /= sample  # 測定回数の範囲内でのnの平均値を算出
    R = R_1 * n / (65536 - n)  # サーミスタの電気抵抗を算出
    T = 1 / (math.log(R/R_a)/B + (1/T_a)) - 273.15  # 温度を算出し単位を絶対温度から摂氏温度に変換

    print("Temperature : {:.1f} deg C".format(T))  # Thonnyのシェルに温度を出力
    print("Resistance  : {:.1f} kΩ\n".format(R))  # Thonnyのシェルに電気抵抗を出力

    oled.fill(0)  # ディスプレイを黒で塗りつぶし
    oled.text("Temperature", 10, 10)  # 左上から横10px、縦10pxの位置にTemperatureと描画
    oled.text("{:.1f} deg C".format(T), 18, 20)  # 左上から横18px、縦20pxの位置に温度の値を描画
    oled.text("Resistance", 10, 36)  # 左上から横10px、縦36pxの位置にResistanceと描画
    oled.text("{:.1f} kilo ohm".format(R), 18, 46)  # 左上から横18px、縦46pxの位置に電気抵抗の値を描画
    oled.show()  # 測定値をディスプレイに表示した後、21行目に戻る
