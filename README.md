# Invasive Species Detection with Deep Learning

This project demonstrates the effectiveness of convolutional neural networks (CNNs) and transfer learning for monitoring invasive species using image data. By leveraging advanced techniques like MobileNet and data augmentation, this study showcases a robust, cost-effective, and scalable approach to biodiversity conservation.

## Key Highlights
- **MobileNet Superiority:** Achieved the highest accuracy of **98.1%**, outperforming traditional CNN architectures.
- **Model Robustness:** Data augmentation and cross-validation were pivotal in addressing challenges like limited dataset size and environmental variability.
- **Model Comparison:** Systematic evaluation of 3-layer and 4-layer CNNs highlighted the trade-off between model complexity and generalization.
- **Scalable Solution:** Automates invasive species identification, providing a scalable and cost-efficient tool for ecological management.

---

## Dataset

The dataset for this project is sourced from the Kaggle: **[Invasive Species Monitoring](https://www.kaggle.com/competitions/invasive-species-monitoring/code)**. 


## How to Use the Dockerfile

### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/invasive-species-detection.git
   cd invasive-species-detection
   ```
2. Build the Docker Image:
   ```bash
   docker build -t invasive-species-detection .
   ```
3. Run the Docker Container
   ```bash
   docker run -p 5000:5000 invasive-species-detection
   ```
   
## Future Directions
- Integration of multi-modal data to improve model accuracy.
- Implementation of dynamic data augmentation for broader ecological applicability.


## Deployed Model on Hugging Face
- [Hugging Face](https://huggingface.co/spaces/MohamedZakaria170/invasive-species-detection)


## Research Paper

The research paper detailing the methods and results of this project is available here:

- [Download PDF](docs/paper.pdf)

