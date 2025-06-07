from __future__ import annotations

from enum import Enum, IntEnum


class Skill(IntEnum):
    Managers = 9
    Professionals = 8
    TechniciansAndAssociateProfessionals = 7
    ClericalSupportWorkers = 6
    ServiceAndSalesWorkers = 5
    SkilledAgriculturalForestryAndFisheryWorkers = 4
    CraftAndRelatedTradesWorkers = 3
    PlantAndMachineOperatorsAndAssemblers = 2
    ElementaryOccupations = 1


class Specialisation(Enum):
    ChiefExecutive = "Chief Executives, Senior Officials, and Legislators"
    AdministrativeManager = "Administrative, and Commercial Managers"
    SpecialisedManager = "Production, and Specialised Services Managers"

    EngineeringProfessional = "Science, and Engineering Professionals"
    HealthProfessional = "Health Professionals"
    TeachingProfessional = "Teaching Professionals"
    BusinessProfessional = "Business, and Administration Professionals"
    ICTProfessional = "Information, and Communications Technology Professionals"
    LegalProfessional = "Legal, Social, and Cultural Professionals"

    EngineeringAssociate = "Science and Engineering Associate Professionals"
    HealthAssociate = "Health Associate Professionals"
    BusinessAssociate = "Business and Administration Associate Professionals"
    LegalAssociate = "Legal, Social, Cultural and Related Associate Professionals"
    ICTTechnician = "Information and Communications Technicians"

    GeneralClerk = "General and Keyboard Clerks"
    CustomerServicesClerk = "Customer Services Clerks"
    RecordingClerk = "Numerical and Material Recording Clerks"
    OtherClericalWorker = "Other Clerical Support Workers"

    PersonalServiceWorker = "Personal Service Workers"
    SalesWorker = "Sales Workers"
    CareWorker = "Personal Care Workers"
    ProtectiveServicesWorker = "Protective Services Workers"

    AgriculturalWorker = "Market-oriented Skilled Agricultural Workers"
    ForestryFisheryHuntingWorker = "Market-Oriented Skilled Forestry, Fishery and Hunting Workers"
    SubsistenceWorker = "Subsistence Farmers, Fishers, Hunters and Gatherers"

    BuildingWorker = "Building and Related Trades Workers (excluding Electricians)"
    MetalWorker = "Metal, Machinery and Related Trades Workers"
    HandicraftWorker = "Handicraft and Printing Workers"
    ElectricalWorker = "Electrical and Electronics Trades Workers"
    CraftWorker = "Food Processing, Woodworking, Garment and Other Craft and Related Trades Workers"

    MachineOperator = "Stationary Plant and Machine Operators"
    Assembler = "Assemblers"
    Driver = "Drivers and Mobile Plant Operators"

    Cleaner = "Cleaners and Helpers"
    AgriculturalLabourer = "Agricultural, Forestry and Fishery Labourers"
    ManufacturingLabourer = "Labourers in Mining, Construction, Manufacturing and Transport"
    FoodPreparationAssistant = "Food Preparation Assistants"
    StreetSalesWorker = "Street and Related Sales and Service Workers"
    RefuseWorker = "Refuse Workers and Other Elementary Workers"


SPECIALISATION_TO_SKILL = {
    Specialisation.ChiefExecutive: Skill.Managers,
    Specialisation.AdministrativeManager: Skill.Managers,
    Specialisation.SpecialisedManager: Skill.Managers,

    Specialisation.EngineeringProfessional: Skill.Professionals,
    Specialisation.HealthProfessional: Skill.Professionals,
    Specialisation.TeachingProfessional: Skill.Professionals,
    Specialisation.BusinessProfessional: Skill.Professionals,
    Specialisation.ICTProfessional: Skill.Professionals,
    Specialisation.LegalProfessional: Skill.Professionals,

    Specialisation.EngineeringAssociate: Skill.TechniciansAndAssociateProfessionals,
    Specialisation.HealthAssociate: Skill.TechniciansAndAssociateProfessionals,
    Specialisation.BusinessAssociate: Skill.TechniciansAndAssociateProfessionals,
    Specialisation.LegalAssociate: Skill.TechniciansAndAssociateProfessionals,
    Specialisation.ICTTechnician: Skill.TechniciansAndAssociateProfessionals,

    Specialisation.GeneralClerk: Skill.ClericalSupportWorkers,
    Specialisation.CustomerServicesClerk: Skill.ClericalSupportWorkers,
    Specialisation.RecordingClerk: Skill.ClericalSupportWorkers,
    Specialisation.OtherClericalWorker: Skill.ClericalSupportWorkers,

    Specialisation.PersonalServiceWorker: Skill.ServiceAndSalesWorkers,
    Specialisation.SalesWorker: Skill.ServiceAndSalesWorkers,
    Specialisation.CareWorker: Skill.ServiceAndSalesWorkers,
    Specialisation.ProtectiveServicesWorker: Skill.ServiceAndSalesWorkers,

    Specialisation.AgriculturalWorker: Skill.SkilledAgriculturalForestryAndFisheryWorkers,
    Specialisation.ForestryFisheryHuntingWorker: Skill.SkilledAgriculturalForestryAndFisheryWorkers,
    Specialisation.SubsistenceWorker: Skill.SkilledAgriculturalForestryAndFisheryWorkers,

    Specialisation.BuildingWorker: Skill.CraftAndRelatedTradesWorkers,
    Specialisation.MetalWorker: Skill.CraftAndRelatedTradesWorkers,
    Specialisation.HandicraftWorker: Skill.CraftAndRelatedTradesWorkers,
    Specialisation.ElectricalWorker: Skill.CraftAndRelatedTradesWorkers,
    Specialisation.CraftWorker: Skill.CraftAndRelatedTradesWorkers,

    Specialisation.MachineOperator: Skill.PlantAndMachineOperatorsAndAssemblers,
    Specialisation.Assembler: Skill.PlantAndMachineOperatorsAndAssemblers,
    Specialisation.Driver: Skill.PlantAndMachineOperatorsAndAssemblers,

    Specialisation.Cleaner: Skill.ElementaryOccupations,
    Specialisation.AgriculturalLabourer: Skill.ElementaryOccupations,
    Specialisation.ManufacturingLabourer: Skill.ElementaryOccupations,
    Specialisation.FoodPreparationAssistant: Skill.ElementaryOccupations,
    Specialisation.StreetSalesWorker: Skill.ElementaryOccupations,
    Specialisation.RefuseWorker: Skill.ElementaryOccupations
}

YEARS_TO_SPECIALISE = {
    Specialisation.ChiefExecutive: 4,
    Specialisation.AdministrativeManager: 4,
    Specialisation.SpecialisedManager: 4,

    Specialisation.EngineeringProfessional: 4,
    Specialisation.HealthProfessional: 5,
    Specialisation.TeachingProfessional: 4,
    Specialisation.BusinessProfessional: 4,
    Specialisation.ICTProfessional: 4,
    Specialisation.LegalProfessional: 4,

    Specialisation.EngineeringAssociate: 4,
    Specialisation.HealthAssociate: 4,
    Specialisation.BusinessAssociate: 4,
    Specialisation.LegalAssociate: 4,
    Specialisation.ICTTechnician: 4,

    Specialisation.GeneralClerk: 3,
    Specialisation.CustomerServicesClerk: 3,
    Specialisation.RecordingClerk: 3,
    Specialisation.OtherClericalWorker: 3,

    Specialisation.PersonalServiceWorker: 3,
    Specialisation.SalesWorker: 3,
    Specialisation.CareWorker: 3,
    Specialisation.ProtectiveServicesWorker: 3,

    Specialisation.AgriculturalWorker: 3,
    Specialisation.ForestryFisheryHuntingWorker: 3,
    Specialisation.SubsistenceWorker: 3,

    Specialisation.BuildingWorker: 3,
    Specialisation.MetalWorker: 3,
    Specialisation.HandicraftWorker: 3,
    Specialisation.ElectricalWorker: 3,
    Specialisation.CraftWorker: 3,

    Specialisation.MachineOperator: 3,
    Specialisation.Assembler: 3,
    Specialisation.Driver: 3,

    Specialisation.Cleaner: 0,
    Specialisation.AgriculturalLabourer: 0,
    Specialisation.ManufacturingLabourer: 0,
    Specialisation.FoodPreparationAssistant: 0,
    Specialisation.StreetSalesWorker: 0,
    Specialisation.RefuseWorker: 0
}
