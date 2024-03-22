#include <OneWire.h>
#include <DallasTemperature.h>

// Pin donde está conectado DQ
const byte pinDatosDQ = 9; // SE PUEDE VER HASTA EN LA PLACA QUE TIENE UN NÚMERO 9
const int relay = 11; //El relay esta en el pin 11

// Instancia a las clases OneWire y DallasTemperature
OneWire oneWireObjeto(pinDatosDQ); // SE LE DA EL OBJETO DONDE TENEMOS ALMACENADO A DQ
DallasTemperature sensorDS18B20(&oneWireObjeto); // SE PASA LA DIRECCIÓN DE MEMORIA DONDE ESTA ALAMCENADO ESE VOBJETO

void setup() {
  pinMode(relay,OUTPUT); //Configurar S como salida
  Serial.begin(9600); //Abrir el puerto serie a la velocidad de 9600
  
  // Iniciamos el bus 1-Wire
  sensorDS18B20.begin();

  //pinMode(relay, OUTPUT); // Lo declaramos como salida
}

void loop() {
  
  // Mandamos comandos para toma de temperatura a los sensores 
  sensorDS18B20.requestTemperatures(); // TOMA DE TEMPERATURA

  // Leemos y msotramos los datos de los sensores DS18B20
  Serial.println(sensorDS18B20.getTempCByIndex(0)); // LECTURA DE SENSOR QUE TIENE EL NÚMERO 0

  while (Serial.available() > 0) {
    char leerCaracter = Serial.read();

    if (leerCaracter == 'A') {
      digitalWrite(relay, LOW); // Apaga el relay LED del relay Enciende
    } else if (leerCaracter == 'E') {
      digitalWrite(relay, HIGH); // Enciende el relay LED del relay Apaga
    }
    // Puedes agregar más casos según tus necesidades

    // Si se recibe cualquier otro carácter, no se hace nada con el relay
  }
  
  delay(1000); // RETARDO DE 1 SEGUNDO

}