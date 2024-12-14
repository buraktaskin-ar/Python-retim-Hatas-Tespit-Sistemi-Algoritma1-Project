# Bead Processing Program
# This program processes multiple boxes of beads, analyzing their weights to detect production errors and gather statistics.

def get_positive_integer(prompt, min_value):
    """
    Prompt the user to enter a positive integer greater than or equal to min_value.
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"The value must be at least {min_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_bead_weights(num_beads):
    """
    Prompt the user to enter weights for the specified number of beads.
    """
    weights = []
    unique_weights = []
    for i in range(num_beads):
        while True:
            try:
                weight = int(input(f"Enter the weight of bead {i+1} (mg): "))
                weights.append(weight)
                if weight not in unique_weights:
                    unique_weights.append(weight)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return weights, unique_weights

def analyze_weights(weights, unique_weights):
    """
    Analyze the weights to determine if there's a production error or identify the unique bead.
    """
    if len(unique_weights) == 1:
        return {'status': 'consistent', 'weight': unique_weights[0]}
    elif len(unique_weights) == 2:
        count_first = weights.count(unique_weights[0])
        count_second = weights.count(unique_weights[1])
        if count_first == 1 or count_second == 1:
            if count_first == 1:
                unique_weight = unique_weights[0]
                standard_weight = unique_weights[1]
            else:
                unique_weight = unique_weights[1]
                standard_weight = unique_weights[0]
            difference = unique_weight - standard_weight
            percentage = (abs(difference) / standard_weight) * 100
            return {
                'status': 'unique',
                'unique_weight': unique_weight,
                'standard_weight': standard_weight,
                'difference': difference,
                'percentage': percentage
            }
        else:
            return {'status': 'error'}
    else:
        return {'status': 'error'}

def main():
    # Initialize statistics
    total_beads = 0
    accepted_beads = 0
    total_boxes = 0
    production_error_boxes = 0
    heaviest_bead_weight = 0
    most_beads_in_box = 0
    max_weight_difference = 0
    heaviest_in_consistent_boxes = 0
    bead_weight_in_most_beads_box = 0

    continue_processing = True

    while continue_processing:
        print("\nStarting to process a new box.")
        num_beads = get_positive_integer("Enter the number of beads in the box (minimum 4): ", 4)
        weights, unique_weights = get_bead_weights(num_beads)

        analysis = analyze_weights(weights, unique_weights)

        if analysis['status'] == 'consistent':
            print("All beads have the same weight.")
            accepted_beads += num_beads

            # Update most beads in a consistent box
            if num_beads > most_beads_in_box:
                most_beads_in_box = num_beads
                bead_weight_in_most_beads_box = analysis['weight']

            # Update heaviest bead in consistent boxes
            if analysis['weight'] > heaviest_bead_weight:
                heaviest_bead_weight = analysis['weight']
                heaviest_in_consistent_boxes = num_beads

        elif analysis['status'] == 'unique':
            unique_weight = analysis['unique_weight']
            standard_weight = analysis['standard_weight']
            difference = analysis['difference']
            percentage = analysis['percentage']

            if difference > 0:
                print(f"The unique bead weighs: {unique_weight} mg")
                print(f"The unique bead is {difference} mg heavier than the others.")
                print(f"The unique bead is %{percentage:.2f} heavier than the others.")
            else:
                print(f"The unique bead weighs: {unique_weight} mg")
                print(f"The unique bead is {abs(difference)} mg lighter than the others.")
                print(f"The unique bead is %{percentage:.2f} lighter than the others.")

            accepted_beads += num_beads

            # Update maximum weight difference
            if abs(difference) > max_weight_difference:
                max_weight_difference = abs(difference)

        else:
            print("Production error detected.")
            production_error_boxes += 1

        total_beads += num_beads
        total_boxes += 1

        # Prompt to continue or exit
        while True:
            user_input = input("Do you want to continue? (E/H): ").strip().lower()
            if user_input == 'e':
                break
            elif user_input == 'h':
                continue_processing = False
                break
            else:
                print("Invalid input. Please enter 'E' to continue or 'H' to exit.")

    # Calculate statistics
    error_percentage = (production_error_boxes / total_boxes) * 100 if total_boxes else 0
    rejected_beads = total_beads - accepted_beads

    # Final Report
    print("\n--- Report ---")
    print(f"Total number of boxes: {total_boxes}")
    print(f"Number of boxes with production errors: {production_error_boxes}")
    print(f"Error rate: %{error_percentage:.2f}")
    print(f"Total number of beads: {total_beads}")
    print(f"Number of accepted beads: {accepted_beads}")
    print(f"Number of rejected beads: {rejected_beads}")
    print(f"Box with the most beads among consistent boxes: {most_beads_in_box} beads")
    print(f"Weight of beads in the box with the most beads: {bead_weight_in_most_beads_box} mg")
    print(f"Heaviest bead weight among consistent boxes: {heaviest_bead_weight} mg")
    print(f"Number of beads in the box with the heaviest beads: {heaviest_in_consistent_boxes}")
    print(f"Maximum weight difference between unique and standard beads: {max_weight_difference} mg")

if __name__ == "__main__":
    main()
