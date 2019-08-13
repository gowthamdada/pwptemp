from math import pi
from WellPath import wellpath

class WellTemperature(object):
    def __init__(self, temp_dict):
        self.tin = temp_dict["tin"]  # Inlet Fluid temperature, °C
        self.ts = temp_dict["ts"]  # Surface Temperature (RKB), °C
        self.xi = 5  # number of radial sections (Inside DS, DS wall, Annular, Csg and Surrounding Space)
        self.wd = temp_dict["wd"]  # Water Depth, m
        deltaz=wellpath(1)[2]  # deltaz is always the same  # Length of each grid cell
        self.riser = round(self.wd / deltaz)  # number of grid cells for the riser
        # Wellbore Geometry
        self.ddi = temp_dict["ddi"]  # Drill String Inner  Diameter, m
        self.ddo = temp_dict["ddo"]  # Drill String Outer Diameter, m
        self.dcsg = temp_dict["dcsg"]  # Casing Inner Diameter, m
        self.dsr = temp_dict["dsr"]  # Surrounding Space Inner Diameter, m
        self.dsro = temp_dict["dsro"]  # Surrounding Space Outer Diameter, m
        self.dri = temp_dict["dri"]  # Riser diameter Inner Diameter, m
        self.dro = temp_dict["dro"]  # Riser diameter Outer Diameter, m
        self.dfm = temp_dict["dfm"]  # Undisturbed Formation Diameter, m
        self.r1 = self.ddi / 2  # Drill String Inner  Radius, m
        self.r2 = self.ddo / 2  # Drill String Outer Radius, m
        self.r3 = self.dcsg / 2  # Casing Inner Radius, m
        self.r3r = self.dri / 2  # Riser Inner Radius, m
        self.r4r = self.dro / 2  # Riser Outer Radius, m
        self.r4 = self.dsr / 2  # Surrounding Space Inner Radius m
        self.r5 = self.dsro / 2  # Surrounding Space Outer Radius, m
        self.rfm = self.dfm / 2  # Undisturbed Formation Radius, m
    # Flow Rate
        self.q = temp_dict["q"]     # Flow rate, m^3/h
        self.va = (self.q / (pi * ((self.r3 ** 2) - (self.r2 ** 2)))) / 3600        # Fluid velocity through the annular
        self.vp = (self.q / (pi * (self.r1 ** 2))) / 3600       # Fluid velocity through the drill pipe
    # Heat Coefficients
    # Thermal Conductivity, W/(m*°C)
        self.lambdal = temp_dict["lambdal"]     # Fluid
        self.lambdac = temp_dict["lambdac"]     # Casing
        self.lambdad = temp_dict["lambdad"]     # Drill Pipe
        self.lambdacsr = temp_dict["lambdacsr"]     # Comprehensive Casing - Surrounding space
        self.lambdasr = temp_dict["lambdasr"]       # Surrounding space
        self.lambdafm = temp_dict["lambdafm"]       # Formation
        self.lambdasrfm = temp_dict["lambdasrfm"]       # Comprehensive Surrounding space - Formation
        self.lambdar = temp_dict["lambdar"]     # Riser
        self.lambdarw = temp_dict["lambdarw"]       # Comprehensive Riser - Seawater 
        self.lambdaw = temp_dict["lambdaw"]     # Seawater
    # Specific Heat Capacity, J/(kg*°C)
        self.cl = temp_dict["cl"]       # Fluid
        self.cc = temp_dict["cc"]     # Casing
        self.cd = temp_dict["cd"]     # Drill Pipe
        self.cr = temp_dict["cr"]     # Riser
        self.cw = temp_dict["cw"]       # Seawater
        self.csr = temp_dict["csr"]       # Surrounding space
        self.cfm = temp_dict["cfm"]       # Formation
    # Convective Heat Transfer Coefficient, W/(m^2*°C)
        self.h1 = temp_dict["h1"]       # Drill Pipe inner wall
        self.h2 = temp_dict["h2"]       # Drill Pipe outer wall
        self.h3 = temp_dict["h3"]       # Casing inner wall
        self.h3r = temp_dict["h3r"]     # Riser inner wall
    # Densities, kg/m3
        self.rhol = temp_dict["rhol"]       # Fluid
        self.rhod = temp_dict["rhod"]       # Drill Pipe
        self.rhoc = temp_dict["rhoc"]       # Casing
        self.rhor = temp_dict["rhor"]       # Riser
        self.rhofm = temp_dict["rhofm"]     # Formation
        self.rhow = temp_dict["rhow"]       # Seawater
        self.rhosr = temp_dict["rhosr"]     # Surrounding Space
    # Thermal Gradients
        self.gt = temp_dict["gt"] * deltaz  # Geothermal gradient, °C/m
        self.wtg = temp_dict["wtg"] * deltaz  # Seawater thermal gradient, °C/m
    # Operational Parameters    
        self.rpm = temp_dict["RPM"]     # Revolutions per minute
        self.t = temp_dict["T"]     # Torque on the drill string, kN*m
        self.tbit = temp_dict["Tbit"]       # Torque on the bit, kN*m
        self.wob = temp_dict["WOB"]     # Weight on bit, kN
        self.rop = temp_dict["ROP"]     # Rate of Penetration, m/h
        self.an = temp_dict["An"]       # Area of the nozzles, m^2
        self.mdt = temp_dict["mdt"]     # Measured Depth of the Target, m
    # Heat Source Terms
        self.qp = 2*pi * (self.rpm/60) * self.t * 2 * 0.24 * self.rhol * (self.vp ** 2) * (self.mdt / (self.ddi*127.094*10**6)) * (1/0.24**.5)
        self.qa = 0.05*(self.wob*(self.rop/3600)+2*pi*(self.rpm/60)*self.tbit) + (self.rhol/2*9.81)*((self.q/3600)/(0.095*self.an)) \
                + (2*0.3832*self.mdt/((self.r3-self.r2)*(127.094*10**6)))*((2*(0.7+1)*self.va)/(0.7*pi*(self.r3+self.r2)
                * (self.r3-self.r2)**2))**0.7
