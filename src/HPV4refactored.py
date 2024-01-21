from Bio import SeqIO
from collections import Counter
import math
from Levenshtein import distance as levenshtein_distance # pip install python-Levenshtein, for more efficient string comparison, because the library is written in C.

# ideas for improvement
# 1. threads 
# 2. when calculating entropy - if the entropy is bigger than some global variable (that would hold the "best" entropy value), 
# stop the loop and go to the next window position. That initial position could have the entropy value set to infinity. 
# O(n) worst case won't become better, but it will be faster on average.

#hpv dangerous dictionary. It depends on the dataset, so it should be changed accordingly.
hpv_d = {'0': '!HPV16', '1': '!HPV35', '2': '!HPV31', '3': '!HPV33', '4': '!HPV18'}
#hpv not dangerous dictionary
hpv_nd = {'0': 'HPV6', '1': 'HPV11', '2': 'HPV44', '3': 'HPV40', '4': 'HPV43', '5': 'HPV42'}

FILE = "hpv.fasta" # first 5 are dangerous, last 6 are not dangerous (11 total). Multiple sequence alignment.
WINDOW_SIZE = 60
PROBE_SIZE = 30

def read_fasta_file(file_path):
    return [str(record.seq) for record in SeqIO.parse(file_path, "fasta")]

def seq_distance(str_1, str_2):
    return levenshtein_distance(str_1, str_2)

def create_regions(sequence, n):
    regions = []
    for i in range(len(sequence) - n + 1):
        curr_region = sequence[i:i + n]
        regions.append(curr_region)
    return regions

def calculate_column_entropy(column):
    total_chars = len(column)
    char_counts = Counter(column)
    probabilities = {char: count / total_chars for char, count in char_counts.items()}
    # Calculate entropy: -Σ(P(x) * log2(P(x)))
    entropy = -sum(prob * math.log2(prob) for prob in probabilities.values())
    # Add penalty for gaps, because they make variants more likely 
    if '-' in column:
        entropy += 1000

    return entropy

def calculate_region_entropy(regions):
    cumulative_entropy = 0

    for j in range(WINDOW_SIZE):
        column = [regions[i][j] for i in range(len(regions))]
        entropy = calculate_column_entropy(column)
        cumulative_entropy += entropy

    return cumulative_entropy

def calculate_entropy_for_each_region(seq_segments):
    entropy_for_each_region = []
    for j in range(len(seq_segments[0])):
        regions = [sequence[j] for sequence in seq_segments]
        entropy = calculate_region_entropy(regions)
        entropy_for_each_region.append((j, entropy))

    return entropy_for_each_region

def find_smallest_entropy_index(segment_entropies):
    min_entropy_indices = sorted(range(len(segment_entropies)), key=lambda k: segment_entropies[k][1])[:2]
    return min_entropy_indices[0]

def select_regions_with_smallest_entropy(sequence_segments, index_of_smallest_entropy):
    select_regions_with_smallest_entropy = []
    for i in range(len(sequence_segments)):
        select_regions_with_smallest_entropy.append(sequence_segments[i][index_of_smallest_entropy])
    return select_regions_with_smallest_entropy

#For each high-risk human papillomavirus sequence,
#there should be at least one probe in the set, 
#so that there are no more than 2 mismatches between its sequence and the virus sequence.
# All probes should have at least 3 mismatches with ALL sequences of non-dangerous viruses
def create_probe_set(probes_from_select_region, dangerous_count=5, undangerous_count=6):
    probe_set = []

    for region_probes in probes_from_select_region:
        dangerous_hpv = region_probes[:dangerous_count]
        undangerous_hpv = region_probes[dangerous_count:]

        for probe_index in range(len(dangerous_hpv)):
            probe = dangerous_hpv[probe_index]
            has_right_distance_to_dangerous = []
            has_right_distance_to_undangerous = []

            for dangerous_index in range(len(dangerous_hpv)):
                if seq_distance(probe, dangerous_hpv[dangerous_index]) < 2:
                    has_right_distance_to_dangerous.append(dangerous_index)

            for undangerous_index in range(len(undangerous_hpv)):
                if seq_distance(probe, undangerous_hpv[undangerous_index]) > 3:
                    has_right_distance_to_undangerous.append(undangerous_index)

            probe_set.append((probe, has_right_distance_to_dangerous, has_right_distance_to_undangerous))

    return probe_set

def filter_probes(probe_set, dangerous_threshold=0, different_threshold=6):
    return [
        probe_with_info for probe_with_info in probe_set
        if len(probe_with_info[1]) > dangerous_threshold and len(probe_with_info[2]) >= different_threshold
    ]

def remove_subsets(probes):
    result_probes = []

    for i, probe_i in enumerate(probes):
        is_subset = False

        for j, probe_j in enumerate(probes):
            if i != j and set(probe_i[1]).issubset(set(probe_j[1])):
                is_subset = True
                break

        if not is_subset:
            result_probes.append(probe_i)

    return result_probes

def get_minimal_probe_set(detects_dangerous_probes_and_different, target_count=5):
    minimal_probe_set = []
    already_detected_sets_with_some_probe = set()

    for probe_info in detects_dangerous_probes_and_different:
        _, proximity_to_high_risk, _ = probe_info

        detected_sets = set(proximity_to_high_risk) - already_detected_sets_with_some_probe

        if detected_sets:
            is_subset = any(set(proximity_to_high_risk).issubset(set(probe_set[1])) for probe_set in minimal_probe_set)

            if not is_subset:
                minimal_probe_set.append(probe_info)
                already_detected_sets_with_some_probe.update(detected_sets)

                if len(already_detected_sets_with_some_probe) == target_count:
                    break

    return remove_subsets(minimal_probe_set)

def print_probe_set_with_translation(probe_set):
    for i, probe_info in enumerate(probe_set, start=1):
        probe, proximity_to_high_risk, distinctiveness_from_low_risk = probe_info

        translated_high_risk_types = [hpv_d[str(idx)] for idx in proximity_to_high_risk]
        translated_low_risk_types = [hpv_nd[str(idx)] for idx in distinctiveness_from_low_risk]

        print(f"Probe {i}:")
        print(f"Sequence: {probe}")
        print(f"Detects High-Risk HPV type: {translated_high_risk_types}")
        print(f"Distinct from Low-Risk HPV: {translated_low_risk_types}")
        print("\n")

# Main Code ----------------------------------------------------------------------------------------------------
        
# tried to use list comprehension, because apperantly its faster than for loops
        
hpv_full_sequences = read_fasta_file(FILE)

sequence_regions = [create_regions(sequence, WINDOW_SIZE) for sequence in hpv_full_sequences]

region_entropies = calculate_entropy_for_each_region(sequence_regions[:5])
index_of_smallest_entropy = find_smallest_entropy_index(region_entropies)

select_regions_with_smallest_entropy_ = select_regions_with_smallest_entropy(sequence_regions, index_of_smallest_entropy)

probes_from_select_region = [create_regions(region, PROBE_SIZE) for region in select_regions_with_smallest_entropy_]
probes_from_select_region = list(zip(*probes_from_select_region)) # transpose, each tuple contains the probes from the same position in different sequences.

probe_set = create_probe_set(probes_from_select_region)
detects_dangerous_probes_and_different = filter_probes(probe_set)
final_probe_set = get_minimal_probe_set(detects_dangerous_probes_and_different)

print_probe_set_with_translation(final_probe_set)

# Main Code ----------------------------------------------------------------------------------------------------
