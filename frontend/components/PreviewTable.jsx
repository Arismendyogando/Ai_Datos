import { useState } from 'react';

export default function PreviewTable({ data }) {
  if (!data) return null;

  return (
    <div className="space-y-8">
      {/* Sección de Información General */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Información del Vendedor</h3>
          <div className="space-y-2">
            <p><span className="font-medium">Nombre:</span> {data.vendor_name}</p>
            <p><span className="font-medium">Dirección:</span> {data.vendor_address}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Información del Cliente</h3>
          <div className="space-y-2">
            <p><span className="font-medium">Nombre:</span> {data.customer_name}</p>
          </div>
        </div>
      </div>

      {/* Detalles de la Factura */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-bold mb-4">Detalles de la Factura</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="font-medium">Número de Factura</p>
            <p>{data.invoice_number}</p>
          </div>
          <div>
            <p className="font-medium">Fecha</p>
            <p>{data.date}</p>
          </div>
          <div>
            <p className="font-medium">Moneda</p>
            <p>{data.currency}</p>
          </div>
          <div>
            <p className="font-medium">Términos de Pago</p>
            <p>{data.payment_terms}</p>
          </div>
        </div>
      </div>

      {/* Tabla de Ítems */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-bold mb-4">Ítems de la Factura</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr>
                <th className="px-4 py-2 border">Descripción</th>
                <th className="px-4 py-2 border">Cantidad</th>
                <th className="px-4 py-2 border">Precio Unitario</th>
                <th className="px-4 py-2 border">Total</th>
              </tr>
            </thead>
            <tbody>
              {data.line_items.map((item, index) => (
                <tr key={index}>
                  <td className="px-4 py-2 border">{item.description}</td>
                  <td className="px-4 py-2 border text-right">{item.quantity}</td>
                  <td className="px-4 py-2 border text-right">{item.unit_price}</td>
                  <td className="px-4 py-2 border text-right">
                    {(item.quantity * item.unit_price).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Totales */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="font-medium">Subtotal</p>
            <p>{(data.total_amount - data.tax_amount).toFixed(2)}</p>
          </div>
          <div>
            <p className="font-medium">Impuestos</p>
            <p>{data.tax_amount}</p>
          </div>
          <div className="col-span-2">
            <p className="font-medium">Total</p>
            <p className="text-xl font-bold">{data.total_amount}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
