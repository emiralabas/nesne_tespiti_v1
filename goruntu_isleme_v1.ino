String gelenVeri = "";

String nesne = "";
int adet = 0;
int guven = 0;

void setup() {

  Serial.begin(115200);
  Serial1.begin(9600);

  Serial.println("Mega basladi!");
}

void loop() {

  if (Serial.available()) {

    gelenVeri = Serial.readStringUntil('\n');
    gelenVeri.trim();

    int ilkVirgul = gelenVeri.indexOf(',');
    int ikinciVirgul = gelenVeri.indexOf(',', ilkVirgul + 1);

    if (ilkVirgul > 0 && ikinciVirgul > ilkVirgul) {

      nesne = gelenVeri.substring(
        0,
        ilkVirgul
      );

      adet = gelenVeri.substring(
        ilkVirgul + 1,
        ikinciVirgul
      ).toInt();

      guven = gelenVeri.substring(
        ikinciVirgul + 1
      ).toInt();

      Serial.print("Nesne: ");
      Serial.println(nesne);

      Serial.print("Adet: ");
      Serial.println(adet);

      Serial.print("Guven: %");
      Serial.println(guven);

      // =========================
      // NEXTION
      // =========================

      Serial1.print("t0.txt=\"");
      Serial1.print(nesne);
      Serial1.print("\"");
      nextionEnd();

      Serial1.print("t1.txt=\"ADET: ");
      Serial1.print(adet);
      Serial1.print("\"");
      nextionEnd();

      Serial1.print("t2.txt=\"GUVEN: %");
      Serial1.print(guven);
      Serial1.print("\"");
      nextionEnd();

      if (nesne == "YOK") {

        Serial1.print("t3.txt=\"DURUM: BEKLENIYOR\"");
        nextionEnd();

      } else {

        Serial1.print("t3.txt=\"DURUM: ALGILANDI\"");
        nextionEnd();
      }
    }
  }
}

void nextionEnd() {

  Serial1.write(0xFF);
  Serial1.write(0xFF);
  Serial1.write(0xFF);
}