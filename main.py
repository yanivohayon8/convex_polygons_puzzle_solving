from src.puzzle import Puzzle


def main():

    puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
    loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                    puzzle_directory + "/ground_truth_rels.csv", 
                    puzzle_directory + "/pieces.csv")
    loader.load()
    pieces = loader.get_final_puzzle()
    print("finish main")

if __name__ == "__main__":
    main()