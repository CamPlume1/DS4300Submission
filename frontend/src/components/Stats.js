import React, {useEffect, useState} from 'react';
import './stats.css';
/*
Component for overall dataset statistics
Created by Cam Plume
 */

const Stats = () => {
  const [transactions, setTransactions] = useState('');
  const [totalSales, setTotalSales] = useState('');
  const [totalUnits, setTotalUnits] = useState('');
  const [countryCount, setCountryCount] = useState('');
  const [topCat, setTopCat] = useState('World War 2 Gliders Asstd Designs');
  const [topRev, setTopRev] = useState('Dotcom Postage')

  useEffect(() => {

      //Working
   const fetchTransaction = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/total_transactions');
        if (response.ok) {
          const data = await response.json();
          setTransactions(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

   //TODO: Fix
   const fetchTopCat = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/top_unit');
        if (response.ok) {
          const data = await response.json();
          setTopRev(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

   const fetchTopRev = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/top_unit_rev');
        if (response.ok) {
          const data = await response.json();
          setTopCat(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

    //working
   const fetchCountryCount = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/countries_count');
        if (response.ok) {
          const data = await response.json();
          setCountryCount(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };


   //Working
   const fetchTotalPrice = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/total_sales');
        if (response.ok) {
          const data = await response.json();
          setTotalSales(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

   //working
   const fetchTotalUnits = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/total_units');
        if (response.ok) {
          const data = await response.json();
          setTotalUnits(data);
        } else {
          console.error('Failed to fetch countries:', response.status);
        }
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

   //TODO: Debug

    fetchTransaction();
    fetchTotalUnits();
    fetchTotalPrice();
    fetchCountryCount();
    fetchTopCat();
    fetchTopRev();

  }, []);

  return (
    <div className="stats">
      <div className="stat-item">In this dashboard we are representing <strong>{transactions}</strong> transactions</div>
      <div className="stat-item">This seller is operating across <strong>{countryCount}</strong> countries</div>
      <div className="stat-item">This seller has sold <strong>${totalSales}</strong> in total goods</div>
      <div className="stat-item">This seller has sold <strong>{totalUnits}</strong> total units</div>
      <div className="stat-item">This seller's top category in units sold is <strong>"{topCat}"</strong></div>
        <div className="stat-item">This seller's top item by revenue is <strong>"{topRev}"</strong> </div>
    </div>
  );
};

export default Stats;
