content = open('../frontend/src/app/components/dashboard/DashboardHome.tsx', 'r', encoding='utf-8').read()

# Find where it cuts off and append the missing ending
ending = ''}}>{a.message}</div>
                  <div style={{ color: "#4B5563", fontSize: "0.68rem", fontFamily: "'JetBrains Mono',monospace", marginTop: 1 }}>{a.created_at}</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.5 }}>
        <div style={{ color: "#8892a4", fontSize: "0.75rem", fontFamily: "'Space Grotesk',sans-serif", fontWeight: 600, letterSpacing: "0.08em", marginBottom: "0.75rem" }}>QUICK ACCESS</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: "0.75rem" }}>
          {MODULES.map((m) => (
            <motion.button key={m.label} onClick={() => navigate(m.path)} whileHover={{ scale: 1.03 }}
              style={{ background: "rgba(11,17,32,0.6)", border: "1px solid rgba(59,130,246,0.1)", borderRadius: 14, padding: "1rem 1.1rem", cursor: "pointer", textAlign: "left", display: "flex", alignItems: "center", gap: "0.75rem" }}>
              <div style={{ color: m.color, background: `${m.color}15`, borderRadius: 10, padding: "0.5rem", flexShrink: 0 }}>{m.icon}</div>
              <div>
                <div style={{ color: "#e8eaf0", fontFamily: "'Space Grotesk',sans-serif", fontWeight: 600, fontSize: "0.85rem" }}>{m.label}</div>
                <div style={{ color: "#4B5563", fontSize: "0.7rem", fontFamily: "'Inter',sans-serif" }}>{m.desc}</div>
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
'''

open('../frontend/src/app/components/dashboard/DashboardHome.tsx', 'w', encoding='utf-8').write(content + ending)
print("Done")