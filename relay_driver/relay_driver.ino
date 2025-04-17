// Simple programme to power a relay off and then on again if signalled on D2
// I'm intending to use this to power off my Allsky camera if the software locks up
// So a companion programme runs on the Pi that sets a GPIO to high when the lockup
// happens, otherwise fixes it to low (the default state).

static int SHUTDOWNWAIT = 30;
static int SLEEPWAIT = 5;
static int STARTUPWAIT = 20;

void setup()
{
  Serial.begin(9600);
  pinMode(2,INPUT);
  pinMode(4, OUTPUT);
}

void loop()
{
  if (digitalRead(2)==LOW)
  {
    digitalWrite(4, HIGH);
    Serial.println("all fine");
  }else{
    Serial.println("waiting for pi to shutdown");
    delay(SHUTDOWNWAIT*1000);
    digitalWrite(4, LOW);
    delay(SLEEPWAIT*1000);
    Serial.println("now retoring power");
    digitalWrite(4, HIGH);
    Serial.println("waiting for pi to boot");
    delay(STARTUPWAIT*1000);
    Serial.println("up again");
  }
  delay(2000);
}