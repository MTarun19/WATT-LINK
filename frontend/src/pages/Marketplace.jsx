import React, { useState } from "react";
import {
  Zap,
  TrendingUp,
  DollarSign,
  Users,
  Star,
  PlusCircle,
  Activity,
  History,
  CheckCircle2,
  X,
  ArrowUpRight,
  ArrowDownRight,
  Search
} from "lucide-react";
import "./Marketplace.css";

export default function Marketplace() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedSeller, setSelectedSeller] = useState(null);
  const [tradeSuccess, setTradeSuccess] = useState(false);
  const [isListingModalOpen, setIsListingModalOpen] = useState(false);

  // New Listing Form State
  const [newEnergy, setNewEnergy] = useState("3.5");
  const [newRate, setNewRate] = useState("0.13");

  // Initial Sellers Data
  const [sellers, setSellers] = useState([
    {
      id: 1,
      name: "Villa 104 - Solar Array A",
      rating: 4.9,
      availableEnergy: "4.2 kWh",
      rate: "$0.14 / kWh",
      rawRate: 0.14,
      distance: "0.2 km",
      status: "Active"
    },
    {
      id: 2,
      name: "Sector 7 Micro-Storage",
      rating: 4.8,
      availableEnergy: "12.0 kWh",
      rate: "$0.12 / kWh",
      rawRate: 0.12,
      distance: "0.5 km",
      status: "Active"
    },
    {
      id: 3,
      name: "GreenResidence Node #12",
      rating: 4.7,
      availableEnergy: "2.8 kWh",
      rate: "$0.15 / kWh",
      rawRate: 0.15,
      distance: "0.8 km",
      status: "Active"
    },
    {
      id: 4,
      name: "E-Mobility Hub Hub B",
      rating: 5.0,
      availableEnergy: "25.5 kWh",
      rate: "$0.11 / kWh",
      rawRate: 0.11,
      distance: "1.2 km",
      status: "Active"
    }
  ]);

  // Transaction History
  const [transactions, setTransactions] = useState([
    { id: "TX-9041", partner: "Villa 102", amount: "2.5 kWh", total: "$0.35", type: "Bought", time: "10 mins ago" },
    { id: "TX-9038", partner: "Sector 7 Storage", amount: "5.0 kWh", total: "$0.60", type: "Bought", time: "1 hour ago" },
    { id: "TX-9022", partner: "Community Hub", amount: "8.2 kWh", total: "$1.14", type: "Sold", time: "3 hours ago" }
  ]);

  // Filter sellers based on search
  const filteredSellers = sellers.filter((s) =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleBuyClick = (seller) => {
    setSelectedSeller(seller);
    setTradeSuccess(false);
  };

  const handleExecuteTrade = () => {
    setTradeSuccess(true);
    const newTx = {
      id: `TX-${Math.floor(1000 + Math.random() * 9000)}`,
      partner: selectedSeller.name,
      amount: selectedSeller.availableEnergy,
      total: `$${(parseFloat(selectedSeller.availableEnergy) * selectedSeller.rawRate).toFixed(2)}`,
      type: "Bought",
      time: "Just now"
    };

    setTimeout(() => {
      setTransactions((prev) => [newTx, ...prev]);
    }, 300);
  };

  const handleCreateListing = (e) => {
    e.preventDefault();
    if (!newEnergy || !newRate) return;

    const newSeller = {
      id: Date.now(),
      name: "Your Smart Meter (Node #01)",
      rating: 5.0,
      availableEnergy: `${newEnergy} kWh`,
      rate: `$${parseFloat(newRate).toFixed(2)} / kWh`,
      rawRate: parseFloat(newRate),
      distance: "Local (0.0 km)",
      status: "Active"
    };

    setSellers((prev) => [newSeller, ...prev]);
    setIsListingModalOpen(false);
    setNewEnergy("3.5");
    setNewRate("0.13");
  };

  return (
    <div className="market">
      {/* Header */}
      <div className="market-header">
        <div>
          <h1>P2P Energy Marketplace</h1>
          <p>Autonomous Peer-to-Peer Microgrid Trading & Dynamic Rate Matching</p>
        </div>
        <button onClick={() => setIsListingModalOpen(true)}>
          <PlusCircle size={20} />
          List Excess Energy
        </button>
      </div>

      {/* Summary KPI Cards */}
      <div className="market-cards">
        <div className="stat-card">
          <Zap size={32} />
          <h2>Market Price</h2>
          <h1>$0.13 / kWh</h1>
        </div>
        <div className="stat-card">
          <TrendingUp size={32} />
          <h2>24h Volume</h2>
          <h1>142.8 kWh</h1>
        </div>
        <div className="stat-card">
          <DollarSign size={32} />
          <h2>Grid Savings</h2>
          <h1>$34.20</h1>
        </div>
        <div className="stat-card">
          <Users size={32} />
          <h2>Active Peers</h2>
          <h1>18 Nodes</h1>
        </div>
      </div>

      {/* Sellers Section */}
      <div className="seller-section">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "15px", marginBottom: "20px" }}>
          <h2>Available Energy Offers</h2>
          <div className="search-bar-wrapper">
            <Search size={18} color="var(--text-muted)" />
            <input
              type="text"
              placeholder="Search peer node..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="market-search-input"
            />
          </div>
        </div>

        <div className="seller-grid">
          {filteredSellers.map((seller) => (
            <div className="seller-card" key={seller.id}>
              <div>
                <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "6px" }}>
                  <Star size={22} />
                  <span style={{ color: "var(--amber-rating)", fontWeight: "700" }}>{seller.rating}</span>
                </div>
                <h2>{seller.name}</h2>
                <p>Distance: {seller.distance}</p>
                <p>Available Supply: <strong>{seller.availableEnergy}</strong></p>
                <strong>{seller.rate}</strong>
              </div>
              <button onClick={() => handleBuyClick(seller)}>Buy Energy</button>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Panels */}
      <div className="bottom-grid">
        {/* Market Analytics Panel */}
        <div className="panel">
          <Activity size={28} />
          <h2>Automated Trading Strategy</h2>
          <p>
            WATT AI continually optimizes your bid parameters based on localized solar irradiance, neighborhood demand curve forecasts, and battery depth of discharge.
          </p>
          <button onClick={() => alert("WATT AI trading agent re-calibrated successfully!")}>
            Optimize AI Strategy
          </button>
        </div>

        {/* Live Transaction Ledger */}
        <div className="panel">
          <History size={28} />
          <h2>Live Settlement Ledger</h2>
          <ul>
            {transactions.map((tx) => (
              <li key={tx.id}>
                <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                  {tx.type === "Bought" ? (
                    <ArrowDownRight size={18} color="#22c55e" />
                  ) : (
                    <ArrowUpRight size={18} color="#00d4ff" />
                  )}
                  <div>
                    <div style={{ fontWeight: "600", color: "var(--text-main)" }}>{tx.partner}</div>
                    <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{tx.id} • {tx.time}</div>
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontWeight: "700", color: "var(--cyan-primary)" }}>{tx.amount}</div>
                  <div style={{ fontSize: "0.85rem", color: "var(--text-subtle)" }}>{tx.total}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Buy Trade Confirmation Modal */}
      {selectedSeller && (
        <div className="modal-overlay" onClick={() => setSelectedSeller(null)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Confirm Energy Purchase</h3>
              <button className="close-btn" onClick={() => setSelectedSeller(null)}><X size={20} /></button>
            </div>

            {!tradeSuccess ? (
              <div className="modal-body">
                <p>You are initiating a peer-to-peer smart contract settlement with <strong>{selectedSeller.name}</strong>.</p>
                <div className="modal-summary">
                  <div><span>Energy Allocation:</span> <strong>{selectedSeller.availableEnergy}</strong></div>
                  <div><span>Unit Price:</span> <strong>{selectedSeller.rate}</strong></div>
                  <div><span>Smart Contract Fee:</span> <strong>$0.01</strong></div>
                </div>
                <button className="confirm-btn" onClick={handleExecuteTrade}>
                  Confirm & Execute Transfer
                </button>
              </div>
            ) : (
              <div className="modal-body success-state">
                <CheckCircle2 size={48} color="#22c55e" />
                <h4>Transaction Completed!</h4>
                <p>ESP32 Microgrid Gateway switch engaged. Power delivery initiated from <strong>{selectedSeller.name}</strong>.</p>
                <button className="confirm-btn" onClick={() => setSelectedSeller(null)}>
                  Close
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Create Listing Modal */}
      {isListingModalOpen && (
        <div className="modal-overlay" onClick={() => setIsListingModalOpen(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>List Excess Solar / Battery Energy</h3>
              <button className="close-btn" onClick={() => setIsListingModalOpen(false)}><X size={20} /></button>
            </div>
            <form onSubmit={handleCreateListing} className="modal-body">
              <label>
                Available Energy (kWh)
                <input
                  type="number"
                  step="0.1"
                  value={newEnergy}
                  onChange={(e) => setNewEnergy(e.target.value)}
                  className="modal-input"
                  required
                />
              </label>
              <label>
                Target Price Rate ($ / kWh)
                <input
                  type="number"
                  step="0.01"
                  value={newRate}
                  onChange={(e) => setNewRate(e.target.value)}
                  className="modal-input"
                  required
                />
              </label>
              <button type="submit" className="confirm-btn" style={{ marginTop: "15px" }}>
                Publish Offer to Microgrid
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}