class Math:
    @staticmethod
    def knap_sack(max_weight, weights, values, index):
        if index < 0 or max_weight <= 0:
            return 0

        current_value = values[index]
        current_weight = weights[index]

        if current_weight > max_weight:
            return Math.knap_sack(max_weight, weights, values, index - 1)
        else:
            val_with_curr = current_value + Math.knap_sack(
                max_weight - current_weight, weights, values, index - 1
            )
            val_without_curr = Math.knap_sack(max_weight, weights, values, index - 1)
            return max(val_with_curr, val_without_curr)
