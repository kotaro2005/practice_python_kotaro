# Animalクラス（設計図）定義
class   Animal:
    #クラス設定時のコンストラクタ
    def __init__(self, name):
        self.name = name

    #speak関数の定義
    def speak(self): #selfはインスタンス自身を指す
        return f"{self.name}が鳴いています" #f文字列で変数を出力

#Animalクラスからインスタンスを作成
dog = Animal("ボケ") 
#インスタンスのメソッドを実行
print(dog.speak())