# If you have 3 straws, possibly of differing lengths, it may or may not be possible to lay them down so that they form a triangle when their ends are touching. For example, if all of the straws have a length of 6 inches. then one can easily construct an equilateral triangle using them. However, if one straw is 6 inches. long, while the other two are each only 2 inches. long, then a triangle cannot be formed.

# Criteria:
# Only determin Equilateral triangle
# If any one length is greater than or equal to the sum of the other two then the lengths cannot be used to form a triangle
# Use a function called check_triangle(side_a, side_b, side_c) -> bool
# Each side can be on a seperate line
# Print possible on correct triangle and impossible when triangle can't be formed
# Input examples:
# Example 1

# Side A: 6
# Side B: 5
# Side C: 4
# Example 2

# Side A: 3
# Side B: 1
# Side C: 1
# Output examples:
# Possible triangle
# Impossible triangle

def check_triangle(side_a: int, side_b: int, side_c: int) -> bool:
    if side_a + side_b > side_c and side_a + side_c > side_b and side_b + side_c > side_a:
        return True

    return False


def main():
    side_a = int(input("Side A: "))
    side_b = int(input("Side B: "))
    side_c = int(input("Side C: "))

    if check_triangle(side_a, side_b, side_c):
        print("Possible triangle")
    else:
        print("Impossible triangle")


if __name__ == "__main__":
    main()
