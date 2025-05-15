import os
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(_name_)

def load_similarity_data(file_path="similarity_scores.csv"):
    """
    Load similarity scores data from a CSV file.

    Args:
        file_path (str): Path to the CSV file (default is "similarity_scores.csv").

    Returns:
        pd.DataFrame: A DataFrame containing the similarity scores data.
    """
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            logger.info(f"Data loaded from {file_path}")
            return df
        else:
            logger.warning(f"{file_path} does not exist.")
            return pd.DataFrame(columns=["Resume", "Job Description", "Similarity Score"])
    except Exception as e:
        logger.error(f"Error loading similarity data: {e}")
        return pd.DataFrame(columns=["Resume", "Job Description", "Similarity Score"])

def generate_report(similarity_df, output_file="similarity_report.txt"):
    """
    Generate a report containing summary statistics and detailed results.
    
    Args:
        similarity_df (pd.DataFrame): DataFrame containing the similarity scores.
        output_file (str): Path to save the generated report (default is "similarity_report.txt").
    """
    try:
        with open(output_file, 'w') as report_file:
            report_file.write("Similarity Report\n")
            report_file.write("=" * 50 + "\n\n")
            
            # Summary statistics
            avg_score = similarity_df["Similarity Score"].mean()
            max_score = similarity_df["Similarity Score"].max()
            min_score = similarity_df["Similarity Score"].min()
            top_match = similarity_df.loc[similarity_df["Similarity Score"].idxmax()]
            worst_match = similarity_df.loc[similarity_df["Similarity Score"].idxmin()]
            
            report_file.write(f"Average Similarity Score: {avg_score:.2f}%\n")
            report_file.write(f"Highest Similarity Score: {max_score:.2f}% (Resume: {top_match['Resume']}, Job Description: {top_match['Job Description']})\n")
            report_file.write(f"Lowest Similarity Score: {min_score:.2f}% (Resume: {worst_match['Resume']}, Job Description: {worst_match['Job Description']})\n")
            report_file.write("\nTop Matches:\n")
            top_matches = similarity_df.nlargest(5, 'Similarity Score')
            for index, row in top_matches.iterrows():
                report_file.write(f"- {row['Resume']} -> {row['Job Description']} | Score: {row['Similarity Score']:.2f}%\n")
            report_file.write("\n" + "=" * 50 + "\n\n")
            
            # Detailed results
            report_file.write("Detailed Similarity Results:\n")
            for index, row in similarity_df.iterrows():
                report_file.write(f"{row['Resume']} -> {row['Job Description']} | Score: {row['Similarity Score']:.2f}%\n")
            
            logger.info(f"Report generated and saved to {output_file}")
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")

def save_report_to_csv(similarity_df, output_file="similarity_report.csv"):
    """
    Save the similarity data to a CSV file.
    
    Args:
        similarity_df (pd.DataFrame): DataFrame containing the similarity data.
        output_file (str): Path to save the CSV file (default is "similarity_report.csv").
    """
    try:
        similarity_df.to_csv(output_file, index=False)
        logger.info(f"Report saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving report to CSV: {e}")

# Example usage
if _name_ == "_main_":
    # Load similarity scores data
    similarity_df = load_similarity_data("similarity_scores.csv")
    
    # If data is loaded, generate a report
    if not similarity_df.empty:
        generate_report(similarity_df, "similarity_report.txt")
        save_report_to_csv(similarity_df, "similarity_report.csv")