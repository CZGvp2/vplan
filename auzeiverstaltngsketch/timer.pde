int runtime = -50; // sekunden
int _prev = 0;

boolean paused = false;

float thickness = 20;

void timer() {
  int seconds = runtime % 60;
  int minutes = (runtime / 60) % 60;
  int hours = (runtime / 3600) % 12;
  
  String second_str, minute_str;
  if (abs(seconds) < 10) second_str = '0' + str(abs(seconds));
  else second_str = str(abs(seconds));
  
  if (abs(minutes) < 10) minute_str = '0' + str(abs(minutes));
  else minute_str = str(abs(minutes));
  
  char sign;
  if (runtime > 0) sign = '+';
  else sign = '-';
  
  textAlign(CENTER, CENTER);
  textSize(50);
  
  translate(width/2, height/2);
  
  float diameter = .8*height;
  
  bow(diameter, seconds/60.0);
  bow(diameter-4*thickness, minutes/60.0);
  bow(diameter-8*thickness, hours/12.0);

  fill(255);
  text("T"+sign+hours+":"+minute_str+":"+second_str, 0, 0);
  
  if (paused) difficulties();
  
  translate(-width/2, -height/2);
}

void bow(float diameter, float ratio) {
  // Malt einen Bogen
  float rad = TWO_PI * ratio - HALF_PI;
  float angle1 = -HALF_PI;
  float angle2 = rad;
  
  if (rad < -HALF_PI) {
    angle2 = -HALF_PI;
    angle1 = rad;
  }
  
  noStroke();
  fill(255);
  arc(0, 0, diameter, diameter, angle1, angle2, PIE);
  fill(0);
  ellipse(0, 0, diameter-thickness*2, diameter-thickness*2);
}

void difficulties() {
  if (second() % 4 < 2) {
    fill(#FFFFFF);
    rect(-220, -70, 440, 150);
    fill(#FF0000);
    text("Technische\nSchwierigkeiten", 0, 0);
  }
}

void tick() {
  int sec = millis()/1000;
  if (sec > _prev) {
    _prev = sec;
    if (!paused) runtime ++;
  }
}

void togglePaused() {
  paused = !paused;
}
