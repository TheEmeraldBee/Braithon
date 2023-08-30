function"answer"{$150}
function"attempts"{$0}

# Expects $0 to be attempts, $2 to be the question message, and $150 to be the answer to the question
function"check"{
	# Set the correct loop to running
	$1 %1

	[
		/////
		# Print the question
		$2 ^ /
		
		# Get the user input as a string
		$151 input"str"

		# If the answer is correct
		(151=150){
			$1 %0
		}{
			# Remove 1 from the attempts
			r"attempts" -

			(0=1000){
				# The user ran out of lives, exit the loop
				$1 %0
			}{
				# Print the number of attempts left
				p"Incorrect, you have "
				^
				p" attempts left."/
			}
		}

		$1
	]
}

# Set a temp value to 0
$1000 %0

# Give user 5 attempts
$0 %5

# Create The First Question
$2 s"What is the largest animal?"
r"answer" s"Blue Whale"

# Ask the question
r"check"

# Only run the program if the user has lives left
(0>1000){
	$2 s"What is the smallest mammal?"
	r"answer" s"Etruscan Shrew"

	r"check"
}


# If the player has no lives, let them know that they failed.
(0=1000){
	p"You are out of lives, therefore you lose. Sorry!"
	exit
}{
	p"You Win! Great Job"
}
