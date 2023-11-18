# Image Encryption and Decryption using Triple DES (TDES)

* Overview :

This project focuses on securing image data through the use of Triple DES (TDES) encryption and decryption. Triple DES is a symmetric-key block cipher that applies the Data Encryption Standard (DES) algorithm three times to each data block. This provides a higher level of security compared to single DES.

* How it Works
  Key Generation:

Three different keys (K1, K2, K3) are derived from a single key through a key scheduling process.
These keys are then used in the encryption and decryption phases.

Encryption:

The image data is divided into fixed-size blocks.
Each block undergoes the encryption process using the TDES algorithm.
The three keys are applied sequentially to each block, providing a layered encryption.

Decryption:

The encrypted image is divided into blocks.
The decryption process uses the three keys in reverse order to decrypt each block.
Installation

* Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/image-encryption.git
cd image-encryption

* Packages Used:

* Run the Application:

bash
Copy code
npm start

* Features
Triple Layered Security: The use of three keys in TDES provides a robust encryption mechanism.
Configurable: Users can specify input and output files, enhancing flexibility.
Key Management: Keys are managed through a separate key file, allowing for secure key storage and distribution.
Contributing

* Fork the repository
Create a new branch: git checkout -b feature/new-feature
Make your changes and commit them: git commit -m 'Add new feature'
Push to the branch: git push origin feature/new-feature
Submit a pull request

* License
This project is licensed under the MIT License.

* Contact
For questions or suggestions, feel free to contact the project maintainer at nottherealbeast02@gmail.com

* Acknowledgements
The project uses the Node.js crypto library for encryption and decryption.
Special thanks to the TDES encryption algorithm contributors and the open-source community.

--------------------------------------------------------------------------------------------------------------------------------------

Feel free to customize this template based on the specifics of your project and the implementation details of your Triple DES image encryption and decryption application.
