extends Node2D

var SPEED = 2
var ANGULAR_SPEED = 0.1

var move_up = false
var move_down = false
var move_right = false
var move_left = false
var rotate_horario = false
var rotate_antihorario = false

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if move_up or Input.get_action_strength("up"):
		position.y -= SPEED
	if move_down or Input.get_action_strength("down"):
		position.y += SPEED
	if move_left or Input.get_action_strength("left"):
		position.x -= SPEED
	if move_right or Input.get_action_strength("right"):
		position.x += SPEED
	if rotate_horario or Input.get_action_strength("horario"):
		rotation += ANGULAR_SPEED
	if rotate_antihorario or Input.get_action_strength("antihorario"):
		rotation -= ANGULAR_SPEED
		

func _on_up_button_down():
	move_up = true

func _on_down_button_down():
	move_down = true	

func _on_right_button_down():
	move_right = true	

func _on_left_button_down():
	move_left = true	

func _on_horario_button_down():
	rotate_horario = true	

func _on_antihorario_button_down():
	rotate_antihorario = true		
	

func _on_up_button_up():
	move_up = false

func _on_down_button_up():
	move_down = false

func _on_right_button_up():
	move_right = false	

func _on_left_button_up():
	move_left = false

func _on_horario_button_up():
	rotate_horario = false

func _on_antihorario_button_up():
	rotate_antihorario = false

