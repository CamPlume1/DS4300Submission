import React, { useEffect, useState } from 'react';
import '../ImageContainer.css'; // Import CSS file

/*
Component for multiple country comparison
Created by Cam Plume
 */
const ImageComponent = ({ selectedOption }) => {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/nick_graphic/?countries=${selectedOption}`);
        if (response.ok) {
          const blob = await response.blob();
          const imageUrl = URL.createObjectURL(blob);
          setImageSrc(imageUrl);
        } else {
          console.error('Failed to fetch image:', response.status);
        }
      } catch (error) {
        console.error('Error fetching image:', error);
      }
    };

    fetchImage();

    // Cleanup function to revoke the object URL when the component unmounts
    return () => {
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  }, [selectedOption]);

  return (
    <div>
      {imageSrc ? (
        <img src={imageSrc} alt="Tom Graphic" />
      ) : (
        <p>Loading image...</p>
      )}
    </div>
  );
};


const NickContainer = () => {
  const [selectedOption, setSelectedOption] = useState([]);
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/countries');
        if (response.ok) {
          const data = await response.json();
          setCountries(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

    fetchCountries();
  }, []);

  const handleOptionChange = (event) => {
    const selectedOptionsArray = Array.from(event.target.selectedOptions, option => option.value);
    setSelectedOption(selectedOptionsArray);
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Comparison of Annual Sales Across Regions</h1>
      </div>
      <div className="visBox">
      <div className="multiple-drop">
        <select multiple value={selectedOption} onChange={handleOptionChange}>
          <option value={selectedOption}>Select Multiple Countries</option>
          {countries.map(country => (
      <option key={country} value={country}>{country}</option>
    ))}
        </select>
      </div>
      <div className="image-grid-comp">
        <ImageComponent selectedOption={selectedOption} />
      </div>
      </div>
      </div>
  );
};

export default NickContainer;