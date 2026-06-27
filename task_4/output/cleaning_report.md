# Cleaning Report

## Objective

This report documents the cleaning operations performed on the messy student dataset before further analysis.

---

## Cleaning Rules Applied

1. Removed duplicate rows from the dataset.
2. Standardized all domain names to one of:
   - ML
   - Web
   - Electronics
   - Mechanical
3. Converted attendance values into numeric percentages.
4. Converted textual score values (e.g. "nine") into numeric values.
5. Converted textual study hour values (e.g. "two") into numeric values.
6. Converted all heights into centimetres.
7. Converted all weights into kilograms.
8. Renamed:
   - height → height_cm
   - weight → weight_kg
9. Normalized submitted values to either "yes" or "no".
10. Replaced missing numeric values using the median of the respective column.
11. Invalid attendance values (below 0 or above 100) were treated as missing and replaced using the median.

---

## Dataset Issues Found

The provided dataset contained:

- Duplicate student records.
- Missing attendance values.
- Missing score values.
- Missing weight values.
- Mixed domain names (ML, ml, MACHINE LEARNING, etc.).
- Heights stored in both metres and centimetres.
- Weights stored in multiple formats.
- Attendance values stored with and without "%".
- Textual numeric values such as "nine" and "two".
- Invalid attendance values (-10 and 105).
- Inconsistent submitted values (yes, Yes, Y, N).

---

## Validation Checklist

After cleaning:

- Duplicate student IDs removed.
- Attendance values are numeric and within 0–100.
- Score values are numeric.
- Study hours are numeric.
- Height values are stored in centimetres.
- Weight values are stored in kilograms.
- Submitted values contain only "yes" or "no".
- Domain values contain only:
  - ML
  - Web
  - Electronics
  - Mechanical
- Critical columns contain no missing values.

---

## Conclusion

The dataset has been cleaned, standardized, and validated according to the specified cleaning rules. It is now suitable for further analysis and visualization in the subsequent tasks.
